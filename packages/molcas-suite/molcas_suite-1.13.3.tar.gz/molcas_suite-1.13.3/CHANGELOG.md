# Changelog

<!--next-version-placeholder-->

## v1.13.3 (2022-06-08)
### Documentation
* Update readme ([`8c2e7c5`](https://gitlab.com/chilton-group/molcas_suite/-/commit/8c2e7c513fbf8f1bad68409d88f975094b5f2e92))

## v1.13.2 (2022-05-17)
### Fix
* Add support for bugged single aniso timing output ([`dc4203b`](https://gitlab.com/chilton-group/molcas_suite/-/commit/dc4203bfa8830cebe91fc98cdd1a9fad25c9efc9))

## v1.13.1 (2022-05-09)
### Fix
* Fix bug in printing index section to file ([`deee5a1`](https://gitlab.com/chilton-group/molcas_suite/-/commit/deee5a119294bba478ed8389dee765c933aebc28))

## v1.13.0 (2022-05-06)
### Feature
* Add orbital reordering code, and rasorb creation function. update and simplify rotation code ([`fa19259`](https://gitlab.com/chilton-group/molcas_suite/-/commit/fa19259fc466569f0ffec82dd7da266cb32a9035))

### Fix
* Correct terminal colour bleed over ([`bb8920d`](https://gitlab.com/chilton-group/molcas_suite/-/commit/bb8920d0f94cb72beba74a96e07377cb38c837db))
* Correct terminal text colour bleed over ([`50adeb8`](https://gitlab.com/chilton-group/molcas_suite/-/commit/50adeb891c60aa582c73d38183fadfa979c11323))

### Documentation
* Update ref to group wiki page ([`6fceb96`](https://gitlab.com/chilton-group/molcas_suite/-/commit/6fceb96bcd015a037c8546e5621175ac1ed5539e))
* Add comments for RasOrb layout ([`4fad02a`](https://gitlab.com/chilton-group/molcas_suite/-/commit/4fad02a4497d12f1358301f650f45e2c28dbd278))

## v1.12.2 (2022-04-29)
### Fix
* Remove profile and improve pep8 compliance ([`d1c4213`](https://gitlab.com/chilton-group/molcas_suite/-/commit/d1c42130cb38b90e9e909eb6c136a9d3ddd2c588))

### Documentation
* Add hdf5 module load to csf custom install guide ([`161c37f`](https://gitlab.com/chilton-group/molcas_suite/-/commit/161c37f73dbf295bbe54e4dafc7e3a3e6172d5aa))

## v1.12.1 (2022-04-11)


## v1.12.0 (2022-04-11)
### Feature
* Modify max_orb to support 0 and add warning for >100 rasorb files ([`039326c`](https://gitlab.com/chilton-group/molcas_suite/-/commit/039326c394a4f954b60497f5933e9809493273b5))
* Add cli arg and option to limit number of rasorb files saved to disk ([`89939ba`](https://gitlab.com/chilton-group/molcas_suite/-/commit/89939ba91f6dd0a7e3123c1f4af793dbf77bc0ef))

## v1.11.1 (2022-04-06)
### Fix
* Add cutoff for k_max of 12 ([`6b9759f`](https://gitlab.com/chilton-group/molcas_suite/-/commit/6b9759fd0fd4dced5b25943dff04cedcf9e8cd27))

## v1.11.0 (2022-04-05)
### Feature
* Add support for actinides and 1st row transition metals to crys keyword, and tidy up docstrings ([`199d7a2`](https://gitlab.com/chilton-group/molcas_suite/-/commit/199d7a2d95440d1c3f1c371fe2ed6a927952ed33))

## v1.10.1 (2022-04-04)


## v1.10.0 (2022-04-04)
### Feature
* Add option to adjust bz field and add output file to allow comparison of in and out of field CF energies ([`b897f8a`](https://gitlab.com/chilton-group/molcas_suite/-/commit/b897f8a5ab6898485ae6628a64f175cbae33d4da))

## v1.9.0 (2022-04-04)
### Feature
* Add preconditioning of Kramers doublets ([`d01346b`](https://gitlab.com/chilton-group/molcas_suite/-/commit/d01346ba948593ccfc0d7c0b2f22ec29f53d411d))

## v1.8.3 (2022-03-30)


## v1.8.2 (2022-03-28)


## v1.8.1 (2022-03-28)


## v1.8.0 (2022-03-21)
### Feature
* Add cfp evaluator ([`1d42158`](https://gitlab.com/chilton-group/molcas_suite/-/commit/1d42158b18149b593634309c28b8772edf3b8511))

### Fix
* Call parser only once in case of unknown_args parser ([`d309378`](https://gitlab.com/chilton-group/molcas_suite/-/commit/d3093789a9a6417fc9e6a37ecd73aabe1c40e528))
* Fix cli parsing ([`cb508ff`](https://gitlab.com/chilton-group/molcas_suite/-/commit/cb508ff351b25f628ad262e9ae8099726e52b56b))

## v1.7.1 (2022-03-14)
### Fix
* Add MAXORB for nroots>100 ([`f6664f6`](https://gitlab.com/chilton-group/molcas_suite/-/commit/f6664f6f5826ad072d4ebe7adf716c16796f0d63))

## v1.7.0 (2022-03-14)
### Feature
* Add mclr class ([`1cb1f55`](https://gitlab.com/chilton-group/molcas_suite/-/commit/1cb1f55b0baf63d1288ac14b4fbe07665e2efba4))

### Fix
* Revert changes to generate_input ([`aed1197`](https://gitlab.com/chilton-group/molcas_suite/-/commit/aed1197c3f729d6aa57ae4109efeb9788418781f))

## v1.6.1 (2022-03-03)
### Fix
* Amend pymolcas call ([`a0eeea0`](https://gitlab.com/chilton-group/molcas_suite/-/commit/a0eeea03eeb53ce7057101f30b1c5cebd520fff3))

## v1.6.0 (2022-02-22)
### Feature
* Add edipmom extractor ([`3a0af55`](https://gitlab.com/chilton-group/molcas_suite/-/commit/3a0af558a5c8299491737fa3cf42377d1e902945))

## v1.5.0 (2022-02-17)
### Feature
* Add coordinate extractor from rassi.h5 ([`51c4d0d`](https://gitlab.com/chilton-group/molcas_suite/-/commit/51c4d0d2675fc919be9c0b67b345abc3fd91570d))

## v1.4.0 (2022-02-14)
### Feature
* Add extra parsing for rotate if user includes quotation marks in swap string ([`c5bafc9`](https://gitlab.com/chilton-group/molcas_suite/-/commit/c5bafc93a501cdb0a591b4cc560561773729fbf3))

## v1.3.0 (2022-02-04)
### Feature
* Fix default filtering ([`1558dd1`](https://gitlab.com/chilton-group/molcas_suite/-/commit/1558dd11726e4da8aa18d9c6a9f0c8686962a012))

## v1.2.0 (2022-02-01)
### Feature
* Add rotate command ([`522f035`](https://gitlab.com/chilton-group/molcas_suite/-/commit/522f035d0769dc82ea0f3beb95556b468078e373))

### Documentation
* Update help text for rotate command ([`630129a`](https://gitlab.com/chilton-group/molcas_suite/-/commit/630129a768ae0e93eba7e951b69c157cb66a6954))

## v1.1.3 (2022-01-28)


## v1.1.2 (2022-01-28)
### Performance
* Update xyz_py minimum version to include better label indexing removal ([`9b51f09`](https://gitlab.com/chilton-group/molcas_suite/-/commit/9b51f094ecb80caf5d472d06b6901c85757c8213))

## v1.1.1 (2022-01-13)
### Fix
* Delete extra line ([`9108ed6`](https://gitlab.com/chilton-group/molcas_suite/-/commit/9108ed6ab139bc951657f9a57733869f075d0e9b))

## v1.1.0 (2022-01-12)
### Feature
* Wave function spec extractor ([`2059d12`](https://gitlab.com/chilton-group/molcas_suite/-/commit/2059d1239e4c3e09dedd3d98ffe49f52998c18b4))

### Fix
* Preprocess rassi h5 output ([`7fb98c6`](https://gitlab.com/chilton-group/molcas_suite/-/commit/7fb98c68e36a047ce6ce02adf85703bb0b84a6bc))
* Bug fix in single_aniso extractor ([`a061a3f`](https://gitlab.com/chilton-group/molcas_suite/-/commit/a061a3f08f0b24e97c2a1baa20a72db19ebec614))
* Bugs introduced by recent changes ([`fadc441`](https://gitlab.com/chilton-group/molcas_suite/-/commit/fadc4412fbaa605db9e98353d7b46748d23f89c7))

### Documentation
* Documentation of extractors ([`6beb8e6`](https://gitlab.com/chilton-group/molcas_suite/-/commit/6beb8e691971d60f6780d7b915b234983afa7704))

## v1.0.1 (2021-12-07)
### Fix
* Use env_var for submit.sh files rather than hard code ([`7653c0a`](https://gitlab.com/chilton-group/molcas_suite/-/commit/7653c0a09e4fcf7fbe4d491d7063deabed7a9c14))

### Documentation
* Update docs to point to group wiki and emphasise new install process ([`e7d5108`](https://gitlab.com/chilton-group/molcas_suite/-/commit/e7d510857cb01b9c2ab8beb50da9f34f12c17d57))

## v1.0.0 (2021-11-04)

