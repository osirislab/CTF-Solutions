---
author: qu4ckles
comments: true
date: 2015-09-21 11:37+00:00
layout: post
slug: csaw-ctf-airport
title: CSAW CTF 2015 - K_{Stairs}
---

The site has a maze game that you must navigate through. On the `/play` tab, it shows a login screen, so an account is needed to play. Registering for an account, it automatically logs you in. The hint is that you need a compass to iwn, which is 10 tokens. The first account made will have none. However, with each account created, three more tokens are added to the current account compared to your previous account, due to cookies. If someone else tries to login with your credentials, they will not have the same amount of tokens.

Generate multiple accounts by registering over and over. Once > 60 tokens are acquired in the most current account, just play the game. The game has eight types of tiles. Avoid the holes and brick walls, which kill you and damage you, respectively. Lava tiles sometimes cannot be avoided and damage you. Water tiles take extra energy (food) to go through. Use the tokens to buy food when necessary. The mystery tiles, which are sometimes necessary to step on, also randomly kill you. Revive yourself with tokens and continue navigating until you see stairs that resemble a white window shutter, which signifies you win and gives you the flag.

FLAG: `KEY{H0000LY_ST41rRs_S0000_MUCH_SPACE}`
