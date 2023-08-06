# ClickSet

This library permits easy creation of command-line and persistent settings
inside a class utilizing the `click` and `confuse` libraries.

```python
from clickset import Setting
from clickset import ClickParams
from clickset import get_config
import confuse
import click

class MyClass:
    verbose = Setting(
        # confuse storage path
        'general.verbose',

        # click boolean option
        option = ClickParams(
            '--verbose/--quiet',
            help = 'Verbose or Quiet Output'
        )
    )

@click.command
# Load all options set in classes
@Setting.options
def main(**kw):
    # Get the default global confuse configuration singleton
    config = get_config()
    foo = MyClass()
    print(f"verbose: {foo.verbose}")
    assert foo.verbose == kw['verbose']
    assert foo.verbose == config['general']['verbose'].get()

main(['--verbose'])
```
