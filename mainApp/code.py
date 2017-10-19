

def is_member(user, group):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group).exists()
