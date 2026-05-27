# Video Script 2 — How ZIP Compression Works

## Segment Breakdown

### [0:00 - 0:04] Hook
"A 2 megabyte zip file turning into 75 gigabytes is the closest thing computers have to black magic."

### [0:04 - 0:08] Question
"So, how the f*** does that even work?"

### [0:08 - 0:12] Core Concept — Repetition
"It all begins with how computers behave. And they're stupidly repetitive. Same words, same pixels, same patterns everywhere."

### [0:12 - 0:16]
"Zip just hunts for those repeats and kills the duplicates."

### [0:16 - 0:20] Two Algorithms
"Using two simple ideas stitched together. Think of it like this."

### [0:20 - 0:24] LZ Algorithm — Banana Example
"If a file says banana banana banana, zip goes, why store this three times?"

### [0:24 - 0:28] LZ Algorithm (continued)
"LZ keeps one banana and replaces the other two with tiny instructions that say, reuse that banana."

### [0:28 - 0:32] Huffman Algorithm
"Then Huffman takes whatever LZ couldn't turn into repeats and compresses those symbols into even shorter code."

### [0:32 - 0:40] Decompression — Lossless Accuracy
"What's even crazier is when you unzip, the process reverses with 100% accuracy."

### [0:40 - 0:48] Central Directory
"literally bit perfect. And zip stores a map of itself at the very end, telling your computer, here's where everything is. Funny thing is, modern AI uses the same idea"

### [0:48 - 0:52] AI Connection
"to squeeze the whole internet into patterns and unpack them as answers."

### [0:52 - 0:56] Closer
"Meaning zip essentially walked so Transformers could hallucinate."