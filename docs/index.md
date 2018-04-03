---
---

{% raw %}

<span style="color: red; font-weight: bold"> Most of this does not yet
exist. It is here to act like a product specification guiding
development. It is highly subject to change and perpetually at risk of
destruction. In short, go away and come back later. </span>

Eucalypt is a small declarative language for working with structured
data formats like YAML and JSON.

Anywhere you currently use text-based templating to process these
formats or anywhere where you're piping this content through several
different tools or build steps - that’s probably a place where
Eucalypt can help you generate your output more cleanly and with fewer
cognitive somersaults.

Eucalypt is a simple, purely functional language that can be used
quickly and easily from the command line or as a library from within
several popular languages.

It has the following features:
  1. a native syntax that makes common transformations succint and
	 cut-down expression syntax for embedding in YAML files
  2. strong text manipulation capabilities including built-in "grok"
	 operators, regular expressions and interpolation
  3. an ergonomic command line interface and access to environment
	 variables, filesystem, URLs
  4. metadata annotations and numerous extension points

If you're generating or processing YAML or JSON, you should give it a
try.

# A lighting tour of the native syntax

A few micro-examples should help give a flavour of Eucalypt's native
syntax.

Here's a simple one:

```eu
target-zones: ["a", "b", "c"] map("eu-west-1{{%}}")
```

...expands into:

```yaml
target-zones:
  - eu-west-1a
  - eu-west-1b
  - eu-west-1c
```

This example illustrates how we apply transformations like `map`
simply by concatenation.

In this example, `map` is just a two-parameter function. Its first
argument is provided in parentheses and its second argument comes from
the preceding list.

Users of languages like Elixir or OCaml may recognise an implicit `|>`
operator here. Clojure users may see an invisible threading macro.
Note that writing elements next to each other like this gives you the
_reverse_ of what you might expect in Haskell or OCaml: we write `x f`
(or `f(x)`), *not* `f x`.

The string template, `"eu-west-1{{%}}"`, defines a function of one
argument, returning a string. The key ingredients here are the
interpolation syntax `{{...}}` which allows values to be inserted to
the string, and the string anaphora "%" which represents a single
parameter when used in a string literal.

Users of Groovy or Kotlin may recognise an equivalent of the `it`
parameter. Lisp hackers are familiar with anaphoric macros. Clojure
users will recognise the `%`, `%1`, `%2` forms usable in `#(...)`
contexts.

The whole line is a **declaration**.

A **block**, the primary structuring element of Eucalypt is written as
a sequence of such declarations enclosed in braces. Unlike JSON,
commas are not needed to separate declarations. Unlike YAML,
indentation is never significant. Instead, the Eucalypt parser
determines the declarations mainly based on the location of colons.
You could write:

```eu
{ x: 1 increment negate y: 2 }
```

...and Eucalypt would know it's two declarations.

Our `target-zones` property declaration is at the **top level** so is
not surrounded by braces explicitly. Nevertheless it is in a block:
the top level block. You can imagine the braces to be there if you
like.

Finally, on this example, it is good practice to document
declarations. Eucalypt offers an easy way to do that using
**declaration metadata** which we squeeze in between a leading
backtick and the declaration itself:

```eu
` “AZs to deploy alien widgets in”
target-zones: [“a”, “b”, “c”] map(“eu-west-1{{%}}”)
```

Let's look at another small example:

```eu
base(name): {
  resource-name: name
  created: eu.meta.runtime
}

anne: base("Anne") {
  laser-colour: "red"
}

bob: base("Bob") {
  eye-count: 7
}
```

We've introduced a new type of declaration here: `base(name): ...`.
This is a **function declaration**, as opposed to the **property
declaration** we saw in the last example.

Eucalypt also has **operator declarations** and a **splice syntax**
which can appear in blocks but we'll ignore those for now. They are
covered in the user guide.

The function declaration declares a function called `base`, accepting
a single parameter (`name`) and returning a block containing two
property declarations.

Functions are declared in and live in blocks just like any other
declaration but they are omitted when output is generated, so
you won't see them in the YAML or JSON that Eucalypt produces.

The braces in the definition of `base` are there to delimit the
resulting block - *not* to define a function body. A number-valued
function would not need them:

```eu
inc(x): x + 1 # this defines an increment function
```

...nor would any function that returns a block without using a block
literal:

```eu
identity(x): x # this just returns its argument
```

The next important ingredient in this example is *block catenation*.

Blocks can be treated as functions of a single parameter and applied
to arguments by catenation, the effect of which is *block merge*.

So writing one block after another produces a merged block containing
the contents of the second block merged "on top" of the first.

There is much more to be said on block merging, but for now:

```eu
{ a: 1 } { b: 2 }
```

...evaluates to `{ a: 1 b: 2 }`.

and

```eu
{ a: 1 } { a: 2 }
```

...evaluates to `{ a: 2 }`.

So in our example, the resulting YAML would be"

```yaml
anne:
  resource-name: Anne
  created: 2018-04-01 12:00:00
  laser-colour: red

bob:
  resource-name: Bob
  created: 2018-04-01 12:00:00
  eye-count: 7
```

As you can see, `eu.meta.runtime` evaluates to a timestamp. This
metadata is generated once at runtime, not each time the expression is
evaluated. Eucalypt the language is purely functional, although its
driver can perform all sorts of side-effects as input to the
evaluation and as output from the evaluation. For this reason, Anne
and Bob will have the same timestamps.

Block merge can be a useful means of generating common content in
objects. The common content can appear first as in this case, allowing
it to be overridden. Or it couple be applied second allowing it to
override the detail. Or a mixture of both. Many more sophisticated
means of combining block data are available too.

Note though that Eucalypt has nothing like virtual functions. The
functions in scope when an expression is created are the ones that are
applied. So if you redefine an `f` like this, in an overriding block:

```eu
{ f(x): x+1 a: f(2) } { f(x): x-2 }
```

...the definition of `a` will not see it.

```yaml
a: e
```

Block merge is only very loosely related to object oriented
inheritance. Also by default you only get a _shallow_ merge - deep
merges are covered in the user guide.

Just like we have string anaphora for turning simple strings into
string-valued functions we have block anaphora, which use underscore
instead of the percent character. `b: { a: _ }` defines a function,
`b`, of one parameter that returns a block. `b(2)` evaluates to `{ a:
2 }`. Applying a block with anaphora to another block will evaluate
the function defined rather than falling back to block merge which is
really just the default behaviour of applying a block.

Eucalypt does not have a lambda syntax (yet). If anaphora cannot do
what you want, consider using less nesting and defining intermediate
functions explicitly using function declaration syntax.

## Quick tour of the command line

Let's shift now to the pragmatics of using Eucalypt from the command
line.

On macOS you can install the `eu` command line tools using Homebrew
with:

```shell
brew install eucalypt
```

Check the version you are running with:

```shell
eu -v
```

`eu` is intended to be easy to use for common tasks and does its best
to allow you to say what you want succinctly. It should be easy to use
in pipelines in combination with other tools like `jq`.

By default, it runs in **ergonomic** mode which will make a few
assumptions in order to allow you to be a little less explicit. It
also pulls in user-specific declarations from `~/.eucalypt`. For
repeatable builds and scripted usage, it is normally more appropriate
to turn ergonomic mode *off* using the `-B (--batch-mode)` switch.

The simplest usage is to specify a Eucalypt file to evaluate and leave
the default render format (YAML) and output (standard out) alone.

```shell
> eu test.eu
```

In ergonomic mode, `eu` with no arguments will generally be taken to
specify that input is coming from standard in. So the above is
equivalent to:

```shell
> cat test.eu | eu
```

There is a switch to control output format explicitly (`-x yaml`, `x
json`, `x toml`, ...) but for the very common case of requiring JSON
output there is a shortcut:

```shell
> eu test.eu -j
```

You can, of course, redirect standard output to a file but if you
specify the output file explicitly (with `-o`), `eu` will infer the
output format from the extension:

```shell
> eu test.eu -o output.json # broadly equivalent to eu test.eu -j > output.json
```

Small snippets of Eucalypt can be passed in directly using the `-e
(--evaluate)` switch.

```shell
> eu -e '{ a: 8 * 8 }'
```

The fact that Eucalypt makes relatively infrequent use of single
quotes makes this usage straightforward for most shells.

By default, `eu` evaluates the entirety of the loaded source and
render it all as the result, omitting any function values and other
non-renderable content. It is possible to select finer-grained content
for output by several means though:

  1. A declaration in the source may be selected as the main target
	 using the `:main` declaration metadata
  2. **Targets** may be named using the `:target` declaration metadata
	 and those targets can then be specified using the `-t (--target)`
	 option to `eu`
  3. The `-e (--evaluate)` option can be passed in addition to other
	 source file(s) to identify an expression to be rendered (e.g.
	 `eu test.eu -e x.y.z`)

In passing, we should note that `eu`'s ability to read JSON and YAML
natively combined with the last options give a simple way to pick
values out of structured data:

```shell
> aws s3-api list-objects | eu -e 'Objects first'
```

There is much more to this story. For instance `eu` can:

- accept several inputs to be merged together: `eu test1.eu test2.eu
  test3.eu`
- accept YAML and JSON files as pure data to be merged in: `eu
  data.yaml tools.eu`
- accept YAML or JSON annotated with Eucalypt to execute: `eu +data.yzml`
- override the default extensions: `eu +yaml@info.txt`
- automatically use `Eufile` files in the current folder hierarchy

The user guide contains more on all these usages.


{% endraw %}
