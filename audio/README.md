# SYDE 252 Project – Phase 1 sound files (Task 2)

36 clips, all **mono, 16 kHz, 16-bit WAV, 5.7–10.6 s**, with reference transcripts in `manifest.csv`.

Naming: `{male|female|child}_{quiet|noisy}_{1–6}.wav`
- male = adult male, female = adult female, child = child
- quiet = clean speech; noisy = the clean speech + real background noise at **+5 dB SNR** (odd numbers = cafeteria, even = street traffic; see the `noise` column in `manifest.csv`)
- the number counts up within each speaker × environment, in set order: A = 1–2, B = 3–4, C = 5–6
- set A/B/C = one sentence set per candidate design (12 clips each, never repeated across designs); see the `set` column in `manifest.csv`
- **`selected/`** holds the 12 clips in use (set A: `_1` and `_2` of each speaker × condition) with its own `manifest.csv`; the other 24 clips (sets B and C) stay in this folder as backup, and the full `manifest.csv` marks each clip with `selected` = yes/no
- `manifest.csv` lists each clip's current name (`file`) next to its original name (`old_file`, e.g. `setA_M_noisy_1.wav`)
- each set mixes several talkers per category (male: 3 speakers, female: 3 speakers, child: 6 children ages 9–12)

Tip: to stop set difficulty from biasing one design, rotate which set goes with which design across listeners (Latin square).

## Sources and licenses

| Use | Dataset | Exact items | License | Download |
|---|---|---|---|---|
| Male + female adult speech | LibriSpeech **test-clean** (Panayotov et al., 2015) | Male speakers 7176, 1089, 61; female 4446, 1580, 8463 (utterance IDs in manifest) | CC BY 4.0 | https://www.openslr.org/12 (test-clean.tar.gz, 346 MB) |
| Child speech | **speechocean762** (Zhang et al., 2021) | Children ages 9–12, speakers 6121, 5195, 2179, 3208 (girls), 6504, 5072 (boys); only utterances rated accuracy ≥ 9, fluency ≥ 9; two sentences joined per clip with 0.6 s gap | CC BY 4.0 | https://www.openslr.org/101 |
| Background noise | **DEMAND** (Thiemann et al., 2013) | PCAFETER (cafeteria) and STRAFFIC (street traffic), channel 1, 16 kHz | CC BY-SA 3.0 | https://zenodo.org/records/1227121 |

Note: speechocean762 children are non-native (Mandarin L1) English speakers. Free native-English child corpora are rare (MyST, LDC2021S05, needs an LDC licence agreement). Mention this as a limitation, or swap in your own recordings of a child.

## References to add

- V. Panayotov, G. Chen, D. Povey, and S. Khudanpur, "LibriSpeech: An ASR corpus based on public domain audio books," in *Proc. ICASSP*, 2015, pp. 5206–5210.
- J. Zhang *et al.*, "speechocean762: An open-source non-native English speech corpus for pronunciation assessment," in *Proc. Interspeech*, 2021, pp. 3710–3714.
- J. Thiemann, N. Ito, and E. Vincent, "The Diverse Environments Multi-channel Acoustic Noise Database (DEMAND): A database of multichannel environmental noise recordings," *Proc. Meetings on Acoustics*, vol. 19, 035081, 2013.

Built by `build.py` (seed 252, reproducible).
