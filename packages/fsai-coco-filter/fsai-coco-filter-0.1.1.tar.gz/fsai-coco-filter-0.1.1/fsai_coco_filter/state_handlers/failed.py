def state_failed(obj, old_state, new_state):
    if new_state.is_failed():
        print("Failed!")
