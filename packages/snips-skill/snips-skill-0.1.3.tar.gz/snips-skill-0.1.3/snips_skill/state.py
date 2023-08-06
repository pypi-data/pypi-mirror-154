from . mqtt import topic
import re


__all__ = ('StateAwareMixin',)


class StateAwareMixin:
    ''' Mixin for stateful skills.
        Status updates are recorded in-memory from MQTT topics,
        e.g. `status/#`.
        The message payload for status updates is JSON-converted if possible.
        The last known state is available in `self.current_state`.
        Subclasses may define handler methods for particular topics,
        e.g. `on_status_lamp_brightness(payload)`.
    '''
    
    replacements = str.maketrans('-', '_')
    wildcard_map = { '+' : r'([^/]+)', '#' : r'(.*)' }

    def __init__(self):
        'Register topics and the state callcack.'
        
        super().__init__()
        self.current_state = {}

        status_topic = self.get_config().get('status_topic')
        assert status_topic, 'status_topic not found in configuration'

        # Construct topic RE from status topic
        self.topic_pattern = re.compile('/'.join(
            map(lambda part: self.wildcard_map.get(part, part),
                status_topic.split('/'))))
        
        # Subscribe to status updates
        register = topic(status_topic, payload_converter=self.decode_json)
        register(self.update_status)


    @staticmethod
    def update_status(self, _userdata, msg):
        ''' Track the global state,
            and invoke handler methods defined by subclasses
            with the message payload.
        '''
        self.invoke_handlers(
            self.on_status_update(msg.topic, msg.payload),
            msg.payload)


    def on_status_update(self, topic, payload):
        ''' Keep the global state in-memory.
            Returns a path to the updated attribute in `self.current_state`
            when the state has changed, or `None` otherwise.
        '''
        path = '.'.join(self.split_topic(topic)).translate(self.replacements)

        # Update only if the value has changed
        if self.current_state.get(path) != payload:
            self.current_state[path] = payload
            self.log.debug('Updated: %s = %s', path, payload)
            return path
    
    
    def split_topic(self, topic):
        ''' Extract relevant components from a message topic.
            The default implementation extracts all parts
            corresponding to MQTT topic wildcards.
            Subclasses may override this.
        '''
        match = self.topic_pattern.match(topic)
        assert match, 'topic pattern mismatch'
        return [part.lower() for group in match.groups() for part in group.split('/')]

        
    def invoke_handlers(self, path, payload):
        ''' Generic handler for status updates,
            invokes topic specific handlers.
        '''
        if not path: return
        method_name = 'on_%s' % path.replace('.', '_')
        if hasattr(self, method_name):
            handler = getattr(self, method_name)
            self.log.debug('Invoking: %s', method_name)
            handler(payload)
