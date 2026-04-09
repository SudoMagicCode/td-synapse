# TD Synapse

## Summary

TD Synapse is drop in TouchDesigner component that makes it easier to see the current performance metrics of your TouchDesigner project. Rather than viewing these statistics in your project Synapse passes your data over a websocket to a small single page app where you can view your project's metrics. Ideal for situations where you want to keep the rendering load light in your project, or circumstances where your project is operating inside of an engine or other host application. For example, you can embed TD Synapse in your TOX file that's playing on a host media server (Pixera for example) and see your project metrics.

[synapse.sudo.codes](https://synapse.sudo.codes/)

## TDM Installation

If you are using the [TouchDesigner Dependency Manager](https://github.com/SudoMagicCode/TouchDesigner-Dependency-Manager) you can add this component to your local project with a `add package` command.

```shell
tdm add package github.com/SudoMagicCode/td-synapse
```
