% Boxes
% EorlBruder

# Introduction

md2pdf allows the usage of some special fenced boxes. Here we've been inspired by the boxes from [hedgedoc](https://github.com/hedgedoc/hedgedoc).

# Usage

Any block in `:`-fences will create a latex `$nameBox`:

```markdown
:::name
This will create a LaTeX `\begin{nameBox}` and `\end{nameBox}` around this text.
:::
```

We have created some default boxes: info, warning, danger, newsletter and quote.

# Examples

:::info
This is an info-box
:::

:::warning
Warning! This is a warning-box!
:::

:::danger
Oh no! Danger-levels are high!
:::

:::newsletter
Cool and fancy news...
:::

:::quote
This is equivalent to prefixing your text with `>`.
:::