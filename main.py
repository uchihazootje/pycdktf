from cdktf import App
from pycdktf.example_contruct_levels.stacks.construct_levels_stack import MyConstructLevelsStack
from pycdktf.example_functional_construct.stacks.functional_construct_stack import MyFunctionalConstructStack
from pycdktf.example_simple_stack.stacks.simple_stack import MySimpleStack

app = App()
MySimpleStack(app, "pycdktf-cdktf-simple-demo")
# MyFunctionalConstructStack(app, "pycdktf-cdktf-func-demo")
# MyConstructLevelsStack(app, "pycdktf-cdktf-construct-levels-demo")

app.synth()
