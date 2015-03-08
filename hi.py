from datetime import datetime
import gevent
import lymph


class Hi(lymph.Interface):

    def apply_config(self, config):
        super(Hi, self).apply_config(config)
        self.username = config.root.get('username')

    def on_start(self):
        super(Hi, self).on_start()
        now = datetime.now().strftime('%H:%M:%S')
        self.emit(
            'hi.joined',
            {'username': self.username, 'timestamp': now}
        )

    @lymph.event('hi.message')
    def message_received(self, event):
        print('({timestamp}) {username}: {message}'.format(**event.body))

    @lymph.event('hi.joined')
    def user_joined(self, event):
        print('({timestamp}) {username} joined.'.format(**event.body))

