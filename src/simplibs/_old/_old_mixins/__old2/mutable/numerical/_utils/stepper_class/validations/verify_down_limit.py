from simplibs.sentinels import UNSET


def verify_down_limit(self, new_value, raise_exception=False):

    # 1. Kontrola zde je UP limit nastaven
    if self.down_limit is not UNSET and new_value < self.down_limit:

        # 2. Kontrola zda je nastavena akce
        if self.down_limit_action:
            self.down_limit_action()

        # 3. Kontrola zda se má vyvolat výjimka
        if raise_exception:
            raise "Dosaženo spodního limitu"
        return False

    # 4. Potvrzení úspěčné validace
    return True