#!/usr/bin/python3
# coding: utf-8

import random

class CoolStuff:
    def __init__(self) -> None:
        self.stuff = """Tell me and I forget. Teach me and I remember. Involve me and I learn. - Benjamin Franklin
A pessimist is one who makes difficulties of his opportunities and an optimist is one who makes opportunities of his difficulties. - Harry S. Truman
Always remember that you are absolutely unique. Just like everyone else. - Margaret Mead
An unexamined life is not worth living. - Socrates
Challenges are what make life interesting and overcoming them is what makes life meaningful. - Joshua J. Marine
Don't judge each day by the harvest you reap but by the seeds that you plant. - Robert Louis Stevenson
Education is not the filling of a pail but the lighting of a fire. - William Butler Yeats
Every man is a poet when he is in love. - Plato
Genius only means hard-working all one's life. - Mendeleyev
Happiness lies not in the mere possession of money; it lies in the joy of achievement, in the thrill of creative effort. - Franklin Roosevelt
I am a slow walker, but I never walk backwards. - Abraham Lincoln
I can't change the direction of the wind, but I can adjust my sails to always reach my destination. - Jimmy Dean
I didn't fail the test. I just found 100 ways to do it wrong. - Benjamin Franklin
I disapprove of what you say, but I will defend to the death your right to say it. - Voltaire
If I looked compared to others far, is because I stand on giant's shoulder. - Newton
If you can't fly, then run; if you can't run, then walk; if you can't walk, then crawl; but whatever you do, you have to keep moving forward. - Martin Luther King
If you don't like something, change it; if you can't change it, change the way you think about it. - Mary Engelbreit
If you have no critics, you will likely have no success. - Malcolm S. Forbes
If you judge people, you have no time to love them. - Mother Teresa
If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough. - Oprah Winfrey
Imagination is more important than knowledge. - Albert Einstein
Intelligence plus character - that is the goal of real education. -Martin Luther King
It is not how much you do, but how much love you put into the doing that matters. - Mother Teresa
Knowledge is a treasure, but practice is the key to it. - British churchman  Thomas Fuller
Knowledge is power. - Francis Bacon
Life is like riding a bicycle. To keep your balance you must keep moving. - Albert Einstein
Living without an aim is like sailing without a compass. - Alexandre Dumas
Love the life you live. Live the life you love. - Bob Marley
Love well, whip well. - Benjamin Franklin
Never argue with stupid people, they will drag you down to their level and then beat you with experience. - Mark Twain
Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill
The best and most beautiful things in the world cannot be seen or even touched. They must be felt with the heart. - Helen Keller
The first wealth is health. - Ralph Waldo Emerson
The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela
The only thing we have to fear is fear itself. - Franklin Roosevelt
The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle. - Steve Jobs
The ordinary focus on what they're getting. The extraordinary think about who they're becoming. -  Robin Sharma
The past cannot be changed. The future is yet in your power. - Mary Pickford
The purpose of our lives is to be happy. - Dalai Lama
The way to get started is to quit talking and begin doing. - Walt Disney
There are seven things that will destroy us: wealth without work; pleasure without conscience; knowledge without character; religion without sacrifice; politics without principle; science without humanity; business without ethics. - Mahatma Gandhi
Those who dare to fail miserably can achieve greatly. - John F. Kennedy
Try not to become a man of success but rather try to become a man of value. - Albert Einstein
Until we can manage time, we can manage nothing else. - Peter F. Drucker
We must accept finite disappointment, but we must never lose infinite hope. - Martin Luther King
When the whole world is silent, even one voice becomes powerful. - Malala
When we are saying this cannot be accomplished, this cannot be done, then we are short-changing ourselves. My brain, it cannot process failure. It will not process failure. - Kobe Bryant
Where there is a will, there is a way. - Thomas Edison
You have to believe in yourself. That's the secret of success. - Charles Chaplin
You must be the change you want to see in the world. - Gandhi""".split('\n')
        
    def print_choice(self):
        """ @random select a say to print """
        return self.stuff[random.randint(0, len(self.stuff)-1)] + '\n'
