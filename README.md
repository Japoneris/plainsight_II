# Plainsight-II

Plainsight is a steganographic tool to produce genuine-looking message.
Transition between words are used to encode bits.

A detailed blog post is available [here](https://japoneris.neocities.org/tech/2022/09/01/plainsight_v2.html).


## Previous version


A previous version of [plainsight](https://github.com/rw/plainsight) already exists.

I found two (three) issues:

- It is coded in `python2`, and at some point the result depends on python2, i.e. it is not possible to encode the message with python2 and decode it with `python3`, `julia` or any other language.
- Encoding shortcuts: the script works with a tree that describes n-grams learned over a corpus. Because of an abusive node pruning method, the markov chain is denaturated.
- Difficulty to understand the previous code (no documentation + too many pointers manipulation)

The two first issues are described and illustrated in the associated [blog post](https://japoneris.neocities.org/tech/2022/09/01/plainsight_v2.html).
The goals of this re-implementation are:

- to make the outputs language-independent
- to provide a better encoding function
- to make the code easier to understand (we have on average the same number of LoC. However, we have documentation included in) 



# Usage 


## Installation

There is no need for external libraries.

To make the script executable without `python` prefixing, do: `chmod +x run.py`



## Folder organization

- `src/`: where are stored the **scripts**
- `raw/`: where are stored **non-processed corpus**
- `corpus/`: where are stored **processed corpus**
- `examples/`: encoded / decoded messages 

## Examples


### Encoding 

`./run.py encode "Hello world+++" corpus/sherlock_yellow_face.txt --save_path=examples/sherlock_3.txt -v --depth=3`

- will encode message `Hello world+++`
- using corpus `corpus/sherlock_yellow_face.txt`
- will save the result in `examples/sherlock_3.txt.enc`
- `-v`: Will display the generated message at the end
- `--depth=3`: using n-grams

It will generate a text with starting by:

```txt
did you ever meet any one who throws reserve to the city that day but nothing but misery can come of it if you enter that cottage all is over between us i gave a cry of surprise and horror the face which she kept shooting at me like that jack you are free to use our e books for any purpose including commercial exploitation under the pillow it was done well about six weeks ago she came to me that you should learn the truth was still puzzling over it and then in our country home my wife made over all her papers were destroyed
i ll wait in the lane and my wife appeared to abide loyally by our engagement for as far as to order her to one side and we married a few weeks afterwards
how can you tell me everything then said i nodding towards my house he murmured pointing to a case than it deserves kindly whisper norbury in my powers or giving less pains to a case than it deserves kindly whisper norbury in my ear and i were choking and had asked the servant to call her if i had to choose between you and in her manner that her solemn promise was not in the open air for i asked
for god s sake few men were capable of greater muscular effort and he only turned to the nurse and child only just moved in so i have noted of some half dozen cases of the matter it may have some difficulty if on the day before be connected with her the photograph which had probably been demanded from her in america
[...]
```

The encoding function start sentences randomly.
For the same message to encode, you may end-up with multiple solution.
However, the decoding is deterministic, and you will recover the same message in all cases.



### Decoding 

To decode, you need to run a similar command:

`./run.py decode examples/sherlock_3.txt.enc corpus/sherlock_yellow_face.txt --save_path=examples/sherlock_3.txt -v --depth=3`

You need to specify the `depth` / size of the n-grams, the script cannot find it automatically.
Nevertheless:

- if you use a smaller depth, you are likely to see an unreadable result.
- if you use a larger depth, the script is likely to fail (it may see an n-gram that is unvalid)


### Depth Matters

For `depth=2`, I get the code:

```txt
that her name and her as a duplicate after him as a secret which my child died at the whole heart and hands and i tried to see if
```

With another seed:
```txt
did she made us a match to strangers it or two upon his long enough when there is grosvenor mixture at the mystery comes to a few weeks i am afraid
```

This is much shorter, but quite confusing.


For `depth=4`:
 
```txt
did she ever talk of revisiting the place
i implore you not to do this jack she cried with a nervous laugh why i thought that if i could be of any assistance to our new neighbors why do you look at me like that jack you are not angry with me
how do you know that he values it highly i asked
for two days after this i stayed at home and my wife walked out
he was waiting on the platform when we stepped out and we could see that her fingers were trembling as she undid the fastenings of her mantle why i never remember having done such a thing in my life before the fact is that i felt as though i were choking and had a perfect longing for a breath of fresh air i really think that i should have knocked yes of course i should have fainted if i had been less cautious i might have been more wise but i was half crazy with fear that you should learn the truth
one day in early spring he had so far relaxed as to go for a walk that i might think the matter out in the fresh morning air
[...]
```

For `depth=5`:

```txt
did you ever meet any one who knew her in america
i wanted your advice sir i don t know what there was about that face mr holmes but it seemed to send a chill right down my back i was some little way off so that i could not make out the features but there was something unnatural and inhuman about the face that was the impression that i had and i moved quickly forwards to get a nearer view of the person who was watching me but as i did so the face suddenly disappeared so suddenly that it seemed to have been plucked away into the darkness of the room i stood for five minutes thinking the business over and trying to analyze my impressions i could not tell if the face were that of a man or a woman it had been too far from me for that but its color was what had impressed me most it was of a livid chalky white and with something set and rigid about it which was shockingly unnatural so disturbed was i that i determined to see a little more of the new inmates of the cottage i approached and knocked at the door which was instantly opened by a tall gaunt woman with a harsh forbidding face
[...]
```

The largest the depth, the more human looking it is.


You can study tree characteristics with the script `stats.py`

`python3 stats.py corpus/sherlock_yellow_face.txt --depth=4`

The script displays stats about the number of nodes, and the number of children.
We provide a metric, the "encoding power", which is the ratio between encoding nodes (non-zero, and non-one), over the number of non-terminal nodes (non-zero, representing all the possible transition).
With a large depth, the value decrease.

| Depth | Encoding power |
|-------|----------------|
| 2   | 38.68 % | 
| 3   | 20.44 % |
| 4   | 11.94 % | 
| 5   | 8.092 % |
| 6   | 6.078 % |

On average, for one bit, you will need `1/0.06 = 16` words to encode it if the depth of the tree is `6`. (This is not exact, but it gives you an idea of your message length).







# Corpus 

## Where to find corpus ?

True texts:

- [Wiki source (txt exportable)](https://en.wikisource.org/wiki/Main_Page)
- [Corpus data](https://www.corpusdata.org/)
- [English corpore](https://www.english-corpora.org/)

Random:

- [Generating Random Text](http://www.richkni.co.uk/php/text/text.php)
- [Blind text Generator](https://www.blindtextgenerator.com/lorem-ipsum)

## Preprocessing

I made a simple script to exploit `Wiki source` texts.

`python3 preprocessing.py raw/sherlock_yellow_face.txt`

will save it in the `corpus/` folder under the same name.

It removes:

- case
- punctuation
- special characters


