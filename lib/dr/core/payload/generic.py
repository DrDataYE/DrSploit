
class GenericPayload:
    def __init__(self, info=None):
        if info is None:
            info = {}

        super().__init__(**info)
        self.explicit_arch = None
        self.explicit_platform = None
        self.actual_payload = None

    def reset(self):
        self.explicit_arch = None
        self.explicit_platform = None
        self.actual_payload = None

    def generate(self, opts=None):
        self.reset()
        return self.redirect_to_actual('generate', opts)

    def payload(self):
        return self.redirect_to_actual('payload')

    def offsets(self):
        return self.redirect_to_actual('offsets')

    def substitute_vars(self, *args):
        return self.redirect_to_actual('substitute_vars', *args)

    def replace_var(self, *args):
        return self.redirect_to_actual('replace_var', *args)

    def compatible_encoders(self):
        return self.redirect_to_actual('compatible_encoders')

    def compatible_nops(self):
        return self.redirect_to_actual('compatible_nops')

    def handle_connection(self, *args):
        return self.redirect_to_actual('handle_connection', *args)

    def on_session(self, *args):
        return self.redirect_to_actual('on_session', *args)

    def stage_payload(self, *args):
        return self.redirect_to_actual('stage_payload', *args)

    def stage_offsets(self):
        return self.redirect_to_actual('stage_offsets')

    def stager_payload(self):
        return self.redirect_to_actual('stager_payload')

    def stager_offsets(self):
        return self.redirect_to_actual('stager_offsets')

    def stage_over_connection(self):
        return self.redirect_to_actual('stage_over_connection?')

    def generate_stage(self, opts={}):
        return self.redirect_to_actual('generate_stage', opts)

    def handle_connection_stage(self, *args):
        return self.redirect_to_actual('handle_connection_stage', *args)

    def handle_intermediate_stage(self, *args):
        return self.redirect_to_actual('handle_intermediate_stage', *args)

    def stage_prefix(self):
        return self.redirect_to_actual('stage_prefix')

    def set_stage_prefix(self, *args):
        return self.redirect_to_actual('stage_prefix=', *args)

    def set_user_input(self, h):
        self.user_input = h
        if self.actual_payload:
            return self.redirect_to_actual('user_input', h)

    def set_user_output(self, h):
        self.user_output = h
        if self.actual_payload:
            return self.redirect_to_actual('user_output', h)

    def redirect_to_actual(self, name, *args, **kwargs):
        self.find_actual_payload()
        method = getattr(self.actual_payload, name, None)
        if method:
            return method(*args, **kwargs)
        else:
            raise NotImplementedError(f"Method {name} not implemented in actual payload")

    def find_actual_payload(self):
        # Placeholder for logic to find and set the actual payload
        pass

    # Accessor methods for explicit_platform and explicit_arch
    @property
    def explicit_platform(self):
        return self._explicit_platform

    @explicit_platform.setter
    def explicit_platform(self, value):
        self._explicit_platform = value

    @property
    def explicit_arch(self):
        return self._explicit_arch

    @explicit_arch.setter
    def explicit_arch(self, value):
        self._explicit_arch = value

    # Protected attribute
    @property
    def actual_payload(self):
        return self._actual_payload

    @actual_payload.setter
    def actual_payload(self, value):
        self._actual_payload = value
