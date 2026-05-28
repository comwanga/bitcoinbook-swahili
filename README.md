# Kujua Bitcoin — Tafsiri ya Kiswahili

Tafsiri ya Kiswahili ya kitabu *Mastering Bitcoin: Programming the Open Blockchain* (Toleo la 3) na Andreas M. Antonopoulos na David A. Harding.

> **Hali ya sasa:** Rasimu ya kwanza — tafsiri yote imekamilika, inangoja ukaguzi wa ubora.

---

## Yaliyomo

| Faili | Sura | Hali |
|---|---|---|
| `preface.adoc` | Utangulizi | ✅ Tafsiriwa |
| `ch01_intro.adoc` | Sura 1 — Utangulizi wa Bitcoin | ✅ Tafsiriwa |
| `ch02_overview.adoc` | Sura 2 — Muhtasari wa Bitcoin | ✅ Tafsiriwa |
| `ch03_bitcoin-core.adoc` | Sura 3 — Bitcoin Core | ✅ Tafsiriwa |
| `ch04_keys.adoc` | Sura 4 — Funguo, Anwani | ✅ Tafsiriwa |
| `ch05_wallets.adoc` | Sura 5 — Pochi | ✅ Tafsiriwa |
| `ch06_transactions.adoc` | Sura 6 — Miamala | ✅ Tafsiriwa |
| `ch07_authorization-authentication.adoc` | Sura 7 — Idhini na Uthibitisho | ✅ Tafsiriwa |
| `ch08_signatures.adoc` | Sura 8 — Saini za Kidijitali | ✅ Tafsiriwa |
| `ch09_fees.adoc` | Sura 9 — Ada za Miamala | ✅ Tafsiriwa |
| `ch10_network.adoc` | Sura 10 — Mtandao wa Bitcoin | ✅ Tafsiriwa |
| `ch11_blockchain.adoc` | Sura 11 — Mnyororo wa Vitalu | ✅ Tafsiriwa |
| `ch12_mining.adoc` | Sura 12 — Uchimbaji wa Bitcoin | ✅ Tafsiriwa |
| `ch13_security.adoc` | Sura 13 — Usalama wa Bitcoin | ✅ Tafsiriwa |
| `ch14_applications.adoc` | Sura 14 — Programu za Bitcoin | ✅ Tafsiriwa |
| `appa_whitepaper.adoc` | Kiambatisho A — Karatasi Nyeupe ya Satoshi | ✅ Tafsiriwa |
| `appb_errata.adoc` | Kiambatisho B — Makosa katika Karatasi Nyeupe | ✅ Tafsiriwa |
| `appc_bips.adoc` | Kiambatisho C — Mapendekezo ya Uboreshaji wa Bitcoin | ✅ Tafsiriwa |

---

## Kuhusu Tafsiri

- **Mfasiri:** comwanga (msaada wa AI)
- **Chanzo:** [Mastering Bitcoin 3rd Edition](https://github.com/bitcoinbook/bitcoinbook) na Andreas M. Antonopoulos & David A. Harding
- **Umbizo:** AsciiDoc — markup yote ya asili imehifadhiwa (index terms, cross-references, picha, hisabati, misimbo)
- **Lugha:** Kiswahili sanifu

### Istilahi Muhimu za Kiswahili

| Kiingereza | Kiswahili |
|---|---|
| Bitcoin | Bitcoin |
| blockchain | mnyororo wa vitalu |
| block | kitalu |
| transaction | muamala |
| wallet | pochi |
| mining | uchimbaji |
| full node | nodi kamili |
| proof of work | uthibitisho wa kazi |
| hash | heshi |
| key (private/public) | funguo (ya siri / ya umma) |
| address | anwani |
| script | hati |
| signature | saini |
| hard fork | tawi gumu |
| soft fork | tawi laini |
| payment channel | njia ya malipo |
| Lightning Network | Lightning Network |

---

## Kupakua

Toleo la hivi karibuni la PDF linapatikana kwenye [Releases](../../releases).

---

## Kujenga PDF

Unahitaji [Docker](https://www.docker.com/) au Ruby + asciidoctor-pdf.

### Kwa Docker

```bash
docker run --rm -v "$(pwd):/documents" asciidoctor/docker-asciidoctor \
  asciidoctor-pdf -a imagesdir=/documents/bitcoinbook-third_edition_print1/images \
  /documents/swahili/book.adoc -o /documents/kujua-bitcoin-swahili.pdf
```

### Kwa asciidoctor-pdf (Ruby)

```bash
gem install asciidoctor-pdf rouge
asciidoctor-pdf -a imagesdir=./bitcoinbook-third_edition_print1/images \
  swahili/book.adoc -o kujua-bitcoin-swahili.pdf
```

---

## Kuchangia

Ukitaka kusaidia kuboresha tafsiri:

1. Fork repo hii
2. Fanya mabadiliko yako kwenye faili zinazohusika ndani ya `swahili/`
3. Fungua Pull Request ukielezea mabadiliko yako

Tafadhali zingatia [istilahi sanifu](#istilahi-muhimu-za-kiswahili) zilizoorodheshwa hapo juu.

---

## Leseni

Kitabu cha asili kimechapishwa chini ya [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Tafsiri hii inatoa heshima hiyo hiyo.

*© Andreas M. Antonopoulos, David A. Harding. Tafsiri ya Kiswahili: comwanga.*
