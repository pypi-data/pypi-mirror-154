from pyntfy import action 

# TODO: This needs testing.

class BroadcastAction(action.Action):
    """
    Broadcast action implementation. (https://ntfy.sh/docs/publish/#send-android-broadcast)
    """
    def __init__(self, label: str, intent: str='io.heckel.ntfy.USER_ACTION',
                 extras: list=[], clear: bool=False) -> None:
        """
        Broadcast action implementation. (https://ntfy.sh/docs/publish/#send-android-broadcast)

        Arguments:
            label -- Label of the action button in the notification

        Keyword Arguments:
            intent -- Android intent name (default: {'io.heckel.ntfy.USER_ACTION'})
            extras -- Android intent extras (default: {[]})
            clear -- Clear notification after action button is tapped (default: {False})
        """
        super().__init__('broadcast', label, clear)
        self.intent = intent
        self.extras = extras

    def get_short_header(self) -> str:
        return ''

    def __str__(self) -> str:
        # TODO: Extras.
        return f'action={self.action}, label="{self.label}", intent={self.intent}, ' + \
               f'clear={str(self.clear).lower()}'
