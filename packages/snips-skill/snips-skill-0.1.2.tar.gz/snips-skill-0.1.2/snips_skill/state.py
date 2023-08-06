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
    
    replacements = str.maketrans('/-', '__')
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
        self.record_state(msg.topic, msg.payload)
        self.on_status_update(msg.topic, msg.payload)


    def record_state(self, topic, payload):
        'Keep the global state in-memory'
        store = self.current_state
        keys = self.split_topic(topic)
        for key in keys[:-1]:
            if key not in store: store[key] = {}
            store = store[key]
        store[keys[-1]] = payload
        self.log.debug('Updated: %s = %s', '.'.join(keys), payload)
        
        
    def split_topic(self, topic):
        ''' Extract relevant components from a message topic.
            The default implementation extracts all parts of the 
            topic corresponding to a MQTT topic wildcard.
            Subclasses may override this.
        '''
        match = self.topic_pattern.match(topic)
        assert match, 'topic pattern mismatch'
        return [part for group in match.groups() for part in group.split('/')]

        
    def on_status_update(self, topic, payload):
        ''' Generic handler for status updates,
            tries to find and invoke specific handlers.
        '''
        method_name = 'on_%s' % topic.translate(self.replacements)
        if hasattr(self, method_name):
            handler = getattr(self, method_name)
            self.log.debug('Invoking %s', method_name)
            handler(payload)
