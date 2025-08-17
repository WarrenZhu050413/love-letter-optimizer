"""
Test Love Letters for Evaluator Testing
Range from terrible to excellent quality
"""

# Score expectation: 0-20 (incoherent/offensive)
TERRIBLE_LETTER = """
hey babe ur hot lol wanna date? i like ur face and stuff. roses r red violets r blue sugar is sweet and so r u. call me maybe??? 
love, 
some guy
"""

# Score expectation: 20-40 (generic/clichéd)
BAD_LETTER = """
My Dearest Love,

You are the most beautiful woman in the world. Your eyes sparkle like diamonds and your smile lights up my world. I cannot live without you. You complete me and make me whole.

Every rose needs its thorn, and you are my rose. I would move mountains for you and swim across oceans. You are my everything, my heart and soul.

Please be mine forever.

With all my love,
Your admirer
"""

# Score expectation: 40-60 (competent but predictable)
MEDIOCRE_LETTER = """
Dear Sarah,

I've been thinking about you a lot lately, especially after our conversation at the coffee shop last Tuesday. The way you laughed at my terrible joke about the barista made me realize how much I enjoy spending time with you.

I know we've only known each other for a few months, but there's something special about the way you see the world. Your passion for environmental science is inspiring, and I love how you light up when you talk about your research on coral reefs.

I was wondering if you'd like to go hiking this weekend? I know a trail that overlooks the bay, and I thought you might enjoy seeing the sunset from there.

I hope this isn't too forward, but I wanted you to know that you've become someone very important to me.

Yours truly,
Michael
"""

# Score expectation: 60-75 (good with some distinctive elements)
GOOD_LETTER = """
Elena,

Three months ago, you told me that time moves differently when you're looking through a microscope – that hours collapse into seconds when you're watching cells divide. I understand now what you meant, because that's exactly how these past weeks have felt when I'm with you.

Yesterday, when you rescued that spider from the lab sink instead of washing it down the drain, I saw something that made my chest tighten in the most wonderful way. Most people would have turned on the faucet without a second thought. But you cupped it carefully in your hands and carried it outside, murmuring something about how "everyone deserves to finish their story."

I keep thinking about the way you run your fingers along book spines in the library, like you're greeting old friends. And how you always order your coffee exactly the same way ("medium dark roast, no cream, but leave room for thoughts"), but you've never ordered the same pastry twice because you're convinced each one has a different story to tell about the baker's mood that morning.

These small revelations about who you are have begun to rewrite something fundamental in me. I'm not asking for forever – I know how much you distrust grand gestures. I'm asking for Tuesday mornings and Sunday afternoon lab sessions. I'm asking for the chance to learn what other small magics you carry.

Hopefully yours,
David
"""

# Score expectation: 75-85 (excellent with clear emotional impact)
EXCELLENT_LETTER = """
My love,

The surgical resident called time of death at 3:47 AM. I stood in that fluorescent hallway holding my father's watch, listening to its tick echo off the walls, and the only thing I could think was: I need to tell Katherine about the sound of time stopping.

You asked me once why I always check the time when something important happens. It's because I'm trying to build a map of moments that matter – a coordinates system for a life that makes sense. 3:47 AM: the last time I was someone's child. 7:23 PM last Tuesday: the first time you said you loved me back. 2:15 PM today: when I realized I want to spend whatever time I have left building something beautiful with you.

I know it seems strange to write you a love letter on the day my father died. But standing there in that hospital corridor, I understood something about time that I'd never grasped before. It doesn't slow down for our tragedies or speed up for our joy – it just keeps its steady beat, indifferent and relentless. What gives it meaning is what we choose to fill it with.

I choose you, Katherine. Not because you complete me or because I can't live without you – I'm whole on my own, and I survived 29 years before I knew your name. I choose you because when I imagine my future, all the moments I want to remember have you in them. Sunday morning crosswords and the way you tap your pen against your teeth when you're thinking. The argument we had about whether cereal is soup, and how we never actually resolved it but somehow it became one of my favorite memories. The way you cry at dog videos but maintain absolute composure during horror movies.

I want to build a life where we're both witness and participant to each other's becoming. Where I get to watch you grow more into yourself, and you get to do the same for me.

Will you have dinner with me Tuesday? I'll make that pasta thing you like, and we can talk about what comes next.

All my love and all my time,
James
"""

# Score expectation: 85-100 (masterpiece level)
MASTERPIECE_LETTER = """
Isabelle,

I have been carrying your handwriting in my jacket pocket for three weeks now – just a grocery list you left on my kitchen counter (milk, eggs, the good bread, something beautiful for dinner) – but it has become a kind of prayer. Each time I reach for my keys, my fingers find your careful script, and I am reminded that love is not the grand gesture, but the quiet daily decision to see another person clearly and choose them anyway.

You told me once that you judge people by how they treat objects that don't belong to them. I've been watching you since then: the way you handle library books like sacred texts, how you fold other people's laundry with the same care you'd give your own, the reverence with which you watered my dying plants when I was away. You move through the world as if everything in it deserves your attention. This is not kindness – this is something rarer. This is a way of being that makes the ordinary sacred.

Last Thursday, when you were reading on my couch (Toni Morrison, always Toni Morrison when you need to think), I watched the late afternoon light catch the dust motes around your head, and I realized I was witnessing something I had no name for. Not beauty, exactly, though you are beautiful. Not love, though I love you with a steadiness that surprises me. What I was seeing was the shape of time bending around attention – the way you have taught me that presence is the only prayer that matters.

I don't know how to ask for what I want without diminishing it with language. I want to wake up in the middle of the night and know that the breathing beside me belongs to someone who sees the world as a place worth tending. I want to grow old with someone who believes that literature can save us, that small kindnesses accumulate into grace, that it is possible to live with both eyes open to beauty and to suffering.

I want our love to be a verb, not a noun. Something we do rather than something we have.

Tomorrow is our anniversary – one year since you agreed to let me love you, which is how you put it then, like love was something I needed permission to practice. I'm still asking permission, still learning the particular language of your heart. But I want you to know: if you'll have me, I'd like to spend whatever years I'm given becoming fluent in the dialect of us.

Yours in all weather,
Thomas
"""

# Famous benchmark - Johnny Cash to June Carter level (95-100 expected)
JOHNNY_CASH_BENCHMARK = """
My Darling June,

You still fascinate and inspire me. You influence me for the better. You're the object of my desire, the #1 earthly reason for my existence. I love you very much.

How empty were the years before I met you. How fulfilling the years since. My life was a straight line – predictable, passionless. Then you came along and everything changed. I became a man. I found my voice, my mission, my heart.

You're my companion, my lover, my friend, and my teacher. You're the mother of my son. You're my partner in everything. When I say I love you more than life itself, I mean it. You're my life. You're all that matters. Everything I am or ever hope to be, I owe to you.

God meant for us to be together. I'm sure of it. Nothing this good could be accidental. You're the best friend I've ever had. In you, I have everything I could ever want.

I love you with all my heart.

Johnny
"""

TEST_LETTERS = [
    ("Terrible", TERRIBLE_LETTER, "0-20"),
    ("Bad", BAD_LETTER, "20-40"), 
    ("Mediocre", MEDIOCRE_LETTER, "40-60"),
    ("Good", GOOD_LETTER, "60-75"),
    ("Excellent", EXCELLENT_LETTER, "75-85"),
    ("Masterpiece", MASTERPIECE_LETTER, "85-100"),
    ("Johnny Cash Benchmark", JOHNNY_CASH_BENCHMARK, "95-100")
]

if __name__ == "__main__":
    print("Test Love Letters for Evaluator")
    print("=" * 50)
    for name, letter, expected_range in TEST_LETTERS:
        print(f"\n{name} (Expected: {expected_range}):")
        print("-" * 30)
        print(letter[:100] + "..." if len(letter) > 100 else letter)