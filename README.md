# Theorem-Factory

A factory-style game where you **produce theorems by applying natural deduction rules**.

In the example image below, the game shows a proof of the formula **`(a or b) implies (b or a)`**, constructed step by step using logical inference machines.

<img width="1281" height="718" alt="image" src="https://github.com/user-attachments/assets/c6b5194f-e575-47d4-b2c7-1e327dda60df" />


## What is Natural Deduction?

**Natural deduction** is a formal proof system where conclusions are derived from assumptions by applying simple inference rules (such as introduction and elimination rules for logical connectives).

For example, if you have a proof of `a` and a proof of `b`, then the **and-introduction rule** allows you to derive a proof of `a and b`.


## Features

- Implementation of a complete set of natural deduction rules for **propositional logic**
- Formulas without a proof are shown as **circles**
- Theorems depending on assumptions are shown as **triangles**
- Theorems without assumptions are shown as **squares**
- Machine menus showing which formulas are currently inside a machine
- **Pause menu (ESC)**:
  - Save / load game
  - Enable / disable visual debug stuff

## Controls

- **Mouse wheel** – Zoom
- **Right mouse button** – Drag camera
- **Left mouse button** – Enter machine menu / place machines
- **Hold Shift + Left mouse button** – Delete machine


## Future Work

- Improve usability by adding a **guided tutorial mode** that introduces all machines step by step with concrete tasks and goals
- Add more **gameplay elements**, such as progression systems where new machines or features are unlocked by producing certain theorems
- Improve and polish the **visual presentation and graphics**



