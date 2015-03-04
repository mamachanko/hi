import lymph


class Hi(lymph.Interface):

    def apply_config(self, config):
        super(Hi, self).apply_config(config)
        self.username = config.get('username')

    def on_start(self):
        super(Hi, self).on_start()
        self.emit('hi.joined', {'username': self.username})

    @lymph.event('hi.message')
    def receive_message(self, event):
        print('{} {}: {}'.format())
