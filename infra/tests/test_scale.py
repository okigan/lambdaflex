from ..src.scale import stack_exists

def test_stack_exists():
    # Replace 'my-stack' with the name of a stack that exists
    assert stack_exists('my-stack') == True
    # Replace 'nonexistent-stack' with the name of a stack that doesn't exist
    assert stack_exists('nonexistent-stack') == False