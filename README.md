# SABACC
![image](https://github.com/user-attachments/assets/2f676c53-f8a4-44cd-b73e-20603232c723)

A Star Wars Sabacc card game clone using Python and Arcade.

This version of the game is unique in the sense that it mainly uses "drag and drop" functionality, as opposed to buttons and hand options. It is heavily inspired by how solitaire works on Windows and games like that.

The main goal with this version was to create a working drag and drop Sabacc card game that has the basic functionality of the cards, the piles, actions and minimal hand logic. And by that metric, it's doing pretty good.

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Run the game:
   Right now, the main game is deck_test.py

## Card Images

Place all card images in `assets/cards/`, including `Back.png`.


## New Features and Enhancements

1. Card sizes can be adjusted by hitting "i" on the keyboard and open a slider menu

![image](https://github.com/user-attachments/assets/35d6b871-d70f-4f54-b9c9-9f796c821cef)


2. Dice roll to simulate a "Sabacc Shift"

![image](https://github.com/user-attachments/assets/e15c9763-121a-4978-9c36-37062eababc3)

To make the dice go away just click them.

3. Winning hand option at the end of three dice rolls

![image](https://github.com/user-attachments/assets/c89c8142-3d8f-4ec0-9960-6965f8c39c15)

Although please note, the winner is only announced when you click the button. And the button only shows up after 3 dice rolls.

4. Improved "gain/swap" functionality with just drag and drop

![image](https://github.com/user-attachments/assets/d7181935-251a-43a9-b6c5-6f42d14271b0)

(As a note, I currently have it so that the discard pile cannot be drawn from unless a card is swapped)

5. The hand total and scoring seems pretty solid

![image](https://github.com/user-attachments/assets/8e599e5e-6222-4993-a637-42d17412e737)

## Issues and future improvements

1. The hand rankings are very limited and do not yet include the full suite of named hands.
2. There is no player logic, or any way for multiple people to play at the same time. But making "bots" will soon be the next phase.
3. The buttons and a lot of UI is a bit rough, but shouldn't take long to clean up.
4. My god is this file huge. It needs split up and I just haven't done it yet.
5. The other files are either testing programs I created or older versions I just included because why not.
6. No betting yet, because it would be pointless.
7. No player order or indication of turns.
8. The idea of online multiplayer is still the dream, but so far it's a ways away.
9. Python isn't great for online play.
10. Did I mention how big the deck_test.py file is?
11. Cool animations for the Sabacc shift and better announcements
12. The discard pile doesn't automatically have a card added to it. At least this way you can choose to seed it or not.
13. Speaking of the discard pile. If you perform a gain/swap, ie..take a card from and put it in the discard pile and then take a card from the draw pile, the card you drop in the discard may or may not disappear. I think I know why this is happening, but I just haven't fixed it yet.
14. No way to add more players yet.
15. Player and deck/pile positions aren't great, but they aren't bad. Something to work on later.
16. The sabacc shift works as it should, but I haven't extensively tested it.
17. If no sabacc shift happens, it doesn't announce anything. Kinda anti-climatic.
    

## Acknowledgments

- Inspired by the Star Wars universe and the Sabacc card game.
- Built using Python and Arcade library.


