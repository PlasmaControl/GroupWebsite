---
date: 2024-08-16
authors:
  - sinaatalay
categories:
  - News
---

# An example post

This post is written to showcase the capabilities of the new group website: $\LaTeX$
equations, cross-referencing, citations, etc.

<!-- more --> 

Here is some math with $\LaTeX$ (automatically numbered):

$$
\begin{equation}
\underbrace{\mathbb{V}^* \times \cdots \times \mathbb{V}^*} _ {p\text{ times}}\times\underbrace{\mathbb{V} \times \cdots \times \mathbb{V}}_{q\text{ times}} \rarr \mathbb{R}
\end{equation}
$$


$$
\begin{align}
CC^{-1}&=ABB^{-1}A^{-1}\\\\
&= A I A^{-1} \\\\
&= AA^{-1} \\\\
&= I
\end{align}
$$

Also, I can cite papers using bibtex! Here is an example[@Serway2014]. The `bib` file is
stored in the repository [here](https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/bibliography.bib).

What about cross-referncing a figure? See [](#fig-test).

![This is a caption.](https://fastly.picsum.photos/id/588/200/200.jpg?hmac=amAMbyBq8ZvuCFGI8jPIt928PLIRtxNQ33bISsbDAys){ #fig-test }

## The source code of this page

This page is written with Markdown, and it's source code is given below:

```md
---
date: 2024-08-16
authors:
  - sinaatalay
categories:
  - News
---

# An example post

This post is written to showcase the capabilities of the new group website: $\LaTeX$
equations, cross-referencing, citations, etc.

<!-- more --> 

Here is some math with $\LaTeX$ (automatically numbered):

$$
\begin{equation}
\underbrace{\mathbb{V}^* \times \cdots \times \mathbb{V}^*} _ {p\text{ times}}\times\underbrace{\mathbb{V} \times \cdots \times \mathbb{V}}_{q\text{ times}} \rarr \mathbb{R}
\end{equation}
$$


$$
\begin{align}
CC^{-1}&=ABB^{-1}A^{-1}\\\\
&= A I A^{-1} \\\\
&= AA^{-1} \\\\
&= I
\end{align}
$$

Also, I can cite papers using bibtex! Here is an example[@Serway2014]. The `bib` file is
stored in the repository [here](https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/bibliography.bib).

What about cross-referncing a figure? See [](#fig-test).

![This is a caption.](https://fastly.picsum.photos/id/588/200/200.jpg?hmac=amAMbyBq8ZvuCFGI8jPIt928PLIRtxNQ33bISsbDAys){ #fig-test }

## The source code of this page

This page is written with Markdown, and it's source code is given below:
```

\bibliography