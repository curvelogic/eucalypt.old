---
layout: page
title: The philosophy behind Eucalypt, the language
---

{% raw %}

<span style="color: red; font-weight: bold"> Much of this does not yet
exist. The introduction is here to act like a product specification,
guiding development. It is highly subject to change and perpetually at
risk of destruction. In short, go away and come back later. </span>

# The philosophy behind Eucalypt (the language)

Eucalypt, the language, is rather a strange language.

Probably much stranger than you might guess on first acquaintance.

People tend to have fairly deep-seated and inflexible opinions about
programming languages and language design [^1] and they will likely
find something in here that they object to.

However, the design is not unprincipled and it is internally
consistent. Design choices are driven by the primary use case. So it's
worth exploring some of the inspiration and philosophy behind the
language itself.

## Accept crypticality for minimal intrusion

Eucalypt is first and foremost a *tool*, rather than a language. It is
intended to replace generation and transformation processes on
semi-structured data formats. Many or most uses of Eucalypt the
language should just be simple one-liner tags in YAML files, or maybe
eucalypt files that are predominantly data rather than manipulation.

The Eucalypt language is the depth behind these one-liners that allows
Eucalypt to accommodate increasingly ambitious use cases without
breaking the paradigm and reaching for a general purpose scripting
language. [^2]

The importance of one-liners and small annotations and "logic
mark-up", means that Eucalypt often favours concise and cryptic over
wordy and transparent. This is a controversial approach.

- Eucalypt logic should "get out of the way" of the data. Templating
  is attractive precisely because the generating source looks very
  like the result. Template tags are often short (and arguably
  "cryptic" - `{{}}`, `<%= %>`, `[| ]`...) because these are "marking
  up" the data which is the main event. At the same time the tags are
  often "noisy" or visually disruptive to ensure they cannot be
  ignored. Eucalypt logic picks and choose from these expressive
  effects to try and be a sympathetic cohabitee with its accompanying
  data.

- There are many cases where it makes sense to resist offering an
  incomplete understanding in favour of demanding full understanding.
  For example, it is spurious to say that `bind(x, f)` gives more
  understanding of what is going on than `x >>= f` - unless you
  understand the monad abstraction and the role of bind in it, you
  gain nothing from the ideas that the word `bind` conveys when trying
  to understand program text.

- Eucalypt plain ignores the notion that program text should be
  readable as English text. This (well motivated) idea has made a
  resurgence in recent years through the back door of internal DSLs
  and "fluent" Java interfaces [^3]. There is much merit in languages
  supple enough to allow the APIs to approach the natural means of
  expression of the problem domain. However, problem domains often
  have their own technical jargon and notation which suit their
  purpose better than natural language so it cuts both ways. Program
  text should be approachable by its target audience but that does not
  mean it should make no demands of its target audience.

These stances lead directly to several slightly esoteric aspects of
Eucalypt that may be obnoxious to some:

- Eucalypt tends to be operator-heavy. Operators are concise (if
  cryptic) and the full range of unicode is available to call upon.
  Using operators keeps custom logic visually out of the way of the
  data whilst also signposting it to attract closer attention.

- Eucalypt lets you define your own binary operators and specify their
  precedence and associativity (which are applied at a relatively late
  stage in the evaluation pipeline - *operator soup* persists through
  the initial parse). There are no unary or ternary operators.

- For absolute minimal intrusion, merely the act of placing elements
  next to each other ("catenation:), `x f`, is meaningful in Eucalypt.
  By default this is pipeline-order function application, but blocks
  and lists can be applied as functions to make common
  transformations, like block merge, very succinct.

- For even more power, Eucalypt lets you alter the meaning of
  concatenation via *idiot brackets* [^4]. This is modeled after the
  *idiom brackets* that can be used to express applicative styles in
  functional programming [^5]. These also provide an acceptable proxy for
  unary, ternary and other operators too.

- An equivalent reinterpretation of Eucalypt block syntax to provide a
  capability similar to Haskell's `do` notation could follow.

## Cohabitation of code and data

Just like templates, Eucalypt source (or Eucalypt-tagged YAML or JSON)
should be almost entirely data.

The idea behind Eucalypt is to adopt the basic maps-and-arrays
organisation philosophy of these data formats but make the data
*active* - allowing lambdas to live in and amongst it and operate on
it and allowing the data to express dispositions towards its
environment by addition of metadata that controls import, export, and
execution preferences.

Eucalypt therefore collapses the separation of code and data to some
degree. You can run `eu` against a mixture of YAML, JSON and eucalypt
files and all the data and logic appears there together in the same
namespace hierarchy. The namespace hierarchy just *is* the data.

However, code and data aren't unified in the sense of Lisp for
instance. Eucalypt is not homoiconic. The relationship is more like
cohabitation; code lives in amongst the data it operates on but is
stripped out before export.

Nevertheless Eucalypt is heavily inspired by Lisp and aims for a
similar feeling of fluidity though:

- lazy evaluation (encompassing uses of Lisp macros which control
  evaluation order - if is)
- economical syntax and syntactic reinterpretability (idiot brackets)

## Simplicity

- Eucalypt values simplicity in the sense of fewer moving parts (and
  therefore, hopefully, fewer things to go wrong). It values ease of
  use in the sense of offering a rich and powerful toolkit. You may
  not think it achieves either.

- Eucalypt values familiarity more in the "shallower" parts of the
  language where it only requires a couple of mental leaps for the
  average programmer in these areas - (ab)use of catenation being the
  key one.

- However, Eucalypt isn't ashamed of its dusty corners. Dusty corners
  are areas where novices and experts alike can get trapped but
  they're also rich seams for experimentation, innovation and
  discovery[^6]. If you have to venture too far off-piste to find what you
  need, we'll find a way to bring it onto the nursery slopes rather
  than close off the mountain.

{% endraw %}


---

#### Footnotes

[^1]: ...often a result of underfamiliarity with the alternatives.

[^2]: For some reason, I think of this rather like the historical
	passages in The Lord of the Rings; they give a tremendous sense of
	the depth of the world, that everywhere you look there is a rich
	culture and background staring back at you. You trust that it's
	all coherent and all there if you need it but are generally happy
	to be led through the main narrative over the surface of this rich
	mythology.

[^3]: Actually the key benefit of fluent interfaces in Java is they
	offer a cheap user interface for configuration of APIs by
	leveraging your IDE's autocomplete capability. All other benefits
	are orthogonal.

[^4]: Sorry but if I didn't call them that, someone else would.

[^5]: Applicative Programming with Effects, Conor McBride and Ross
	Paterson. (2008)
	http://www.staff.city.ac.uk/~ross/papers/Applicative.html

[^6]: "A man of genius makes no mistakes. His errors are volitional
	and are the portals to discovery." - James Joyce, Ulysses
