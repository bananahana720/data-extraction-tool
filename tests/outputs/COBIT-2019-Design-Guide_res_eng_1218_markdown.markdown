---
title: COBIT-2019-Design-Guide_res_eng_1218
date: "2018-12-07T10:51:08"
source: COBIT-2019-Design-Guide_res_eng_1218.pdf
format: pdf
---

# DESIGN GUIDE

## Designing an Information

## and Technology

## Governance Solution

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

## About ISACA

N earing its 50th year, ISAC A ® (isaca.org) is a global association helping individuals and enterprises achieve the
positive potential of technology. Technology pow ers today’s w orld and ISAC A equips professionals w ith the
know ledge, credentials, education and com m unity to advance their careers and transform  their organizations. ISAC A
leverages the expertise of its half-m illion engaged professionals in inform ation and cyber security, governance,
assurance, risk and innovation, as w ell as its enterprise perform ance subsidiary, C M M I ® Institute, to help advance
innovation through technology. ISAC A has a presence in m ore than 1 88 countries, including m ore than 21 7  chapters
and offices in both the U nited States and C hina.
D isclaim er
ISAC A has designed and created C O B IT ® 2019 D esign G uide: D esigning an Inform ation and Technology
G overnance Solution (the “W ork”) prim arily as an educational resource for enterprise governance of inform ation and
technology (EG IT), assurance, risk and security professionals. ISAC A m akes no claim  that use of any of the W ork
w ill assure a successful outcom e. The W ork should not be considered inclusive of all proper inform ation, procedures
and tests or exclusive of other inform ation, procedures and tests that are reasonably directed to obtaining the sam e
results. In determ ining the propriety of any specific inform ation, procedure or test, enterprise governance of
inform ation and technology (EG IT), assurance, risk and security professionals should apply their ow n professional
judgm ent to the specific circum stances presented by the particular system s or inform ation technology environm ent.
Copyright
©  201 8 ISAC A. All rights reserved.  For usage guidelines, see w w w.isaca.org/C O B ITuse .

# ISACA

1 7 00 E. G olf R oad, Suite 400
Schaum burg, IL 601 7 3, U SA
Phone: + 1 .847 .660.5505
Fax: + 1 .847 .253.1 7 55
C ontact us: https://support.isaca.org
W ebsite: w w w .isaca.org
Participate in the ISA C A  O nline Forum s: https://engage.isaca.org/onlineforum s
Tw itter: http://tw itter.com /ISAC AN ew s
L inkedIn: http://linkd.in/ISAC AO fficial
Facebook: w w w .facebook.com /ISAC AH Q
Instagram : w w w .instagram .com /isacanew s/

# COBIT ® 2019 DESIGN GUIDE

2
C O B IT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution

# ISB N  9 7 8-1 -60420-7 65-1

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

3

# IN  M E M O R IA M : JO H N  LA IN H A RT (1946 -2 0 18)

In M em oriam : John Lainhart (1946 -2 0 18)
D edicated to John Lainhart, ISA C A  B oard chair 19 84-19 85. John w as instrum ental in the creation of the C OB IT ®
fram ew ork and m ost recently served as chair of the w orking group for C OB IT ® 2 019 , w hich culm inated in the
creation of this w ork. Over his four decades w ith ISA C A , John w as involved in num erous aspects of the association
as w ell as holding ISA C A’s C ISA , C R ISC , C ISM  and C G E IT  certifications. John leaves behind a rem arkable
personal and professional legacy, and his efforts significantly im pacted ISA C A .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

P age intentionally left blank
4

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

A cknow ledgm ents
ISA C A  w ishes to recognize:
CO BIT W orking Group (2017-2018)
John Lainhart, C hair, C ISA , C R ISC , C ISM , C G E IT , C IPP/G , C IPP/U S, G rant T hornton, U SA
M att C onboy, C igna, U SA
R on Saull, C G E IT , C SP, G reat-W est Lifeco & IG M  F inancial (retired), C anada
Developm ent Team
Steven D e H aes, Ph.D ., A ntw erp M anagem ent School, U niversity of A ntw erp, B elgium
M atthias G oorden, Pw C , B elgium
Stefanie G rijp, Pw C , B elgium
B art Peeters, Pw C , B elgium
G eert Poels, Ph.D ., G hent U niversity, B elgium
D irk Steuperaert, C ISA , C R ISC , C G E IT , IT  In B alance, B elgium
Expert Review ers
F loris A m pe, C ISA , C R ISC , C G E IT , C IA , ISO2 7000, PR IN C E 2 , T OG A F, Pw C , B elgium
G raciela B raga, C G E IT , A uditor and A dvisor, A rgentina
Jam es L. G olden, G olden C onsulting A ssociates, U SA
J. W inston H ayden, C ISA , C R ISC , C ISM , C G E IT , South A frica
A bdul R afeq, C ISA , C G E IT , F C A , M anaging D irector, W incer Infotech Lim ited, India
Jo Stew art-R attray, C ISA , C R ISC , C ISM , C G E IT , FA C S C P, B R M  H oldich, A ustralia

## ISACA Board of Directors

R ob C lyde, C ISM , C lyde C onsulting LLC , U SA , C hair
B rennan B aybeck, C ISA , C R ISC , C ISM , C ISSP, Oracle C orporation, U SA , V ice-C hair
T racey D edrick, F orm er C hief R isk Officer w ith H udson C ity B ancorp, U SA
Leonard Ong, C ISA , C R ISC , C ISM , C G E IT , C OB IT  5 Im plem enter and A ssessor, C F E , C IPM , C IPT , C ISSP,
C IT B C M , C PP, C SSLP, G C FA , G C IA , G C IH , G SN A , ISSM P-ISSA P, PM P, M erck & C o., Inc., Singapore
R .V . R aghu, C ISA , C R ISC , Versatilist C onsulting India Pvt. Ltd., India
G abriela R eynaga, C ISA , C R ISC , C OB IT  5 F oundation, G R C P, H olistics G R C , M exico
G regory T ouhill, C ISM , C ISSP, C yxtera F ederal G roup, U SA

## T ed W olff, C ISA , Vanguard, Inc., U SA

T ichaona Zororo, C ISA , C R ISC , C ISM , C G E IT , C OB IT  5 A ssessor, C IA , C R M A , E G IT  | E nterprise G overnance

## of IT  (Pty) Ltd, South A frica

T heresa G rafenstine, C ISA , C R ISC , C G E IT , C G A P, C G M A , C IA , C ISSP, C PA , D eloitte & T ouche LLP, U SA ,
ISA C A  B oard C hair, 2 017-2 018
C hris K . D im itriadis, Ph.D ., C ISA , C R ISC , C ISM , IN T R A LOT , G reece, ISA C A  B oard C hair, 2 015-2 017
M att Loeb, C G E IT , C A E , FA SA E , C hief E xecutive Officer, ISA C A , U SA
R obert E  Stroud (19 65-2 018), C R ISC , C G E IT , X ebiaLabs, Inc., U SA , ISA C A  B oard C hair, 2 014-2 015
ISAC A is deeply saddened by the passing of Robert E Stroud in Septem ber 2018.

# A C K N O W LE DG M E N TS

5

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

P age intentionally left blank
6

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# T A B LE O F C O N TEN TS

List of Figures ..................................................................................................................................................1 1
P art I.  D esign P rocess ...........................................................................................................................1 5
C hapter 1 . Introduction and P urpose .......................................................................................1 5
1.1 G overnance S ystem s ....................................................................................................................................15
1.2  S tructure of T his Publication ........................................................................................................................15
1.3  T arget A udience for T his Publication ...........................................................................................................16
1.4 R elated G uidance: C O B IT ® 2019 Im plem entation G uide ...............................................................................16
C hapter 2 . B asic C oncepts: G overnance S ystem  and C om ponents ..........1 7
2 .1 Introduction .................................................................................................................................................17
2 .2  G overnance and M anagem ent Objectives ......................................................................................................18
2 .3  C om ponents of the G overnance S ystem ........................................................................................................2 0
2 .4 F ocus A reas .................................................................................................................................................2 0
2 .5 C apability L evels .........................................................................................................................................2 0
2 .6 D esign F actors .............................................................................................................................................2 1
2 .6.1 W hy is T here no Industry S ector D esign F actor? ....................................................................................2 8
C hapter 3 . Im pact of D esign Factors .......................................................................................2 9
3 .1 Im pact of D esign F actors ..............................................................................................................................2 9
C hapter 4 . D esigning a Tailored G overnance S ystem .............................................31
4.1 Introduction .................................................................................................................................................3 1
4.2  S tep 1: U nderstand the E nterprise C ontext and S trategy ................................................................................3 2
4.2 .1 U nderstand E nterprise S trategy .............................................................................................................3 2
4.2 .2  U nderstand E nterprise G oals .................................................................................................................3 2
4.2 .3  U nderstand the R isk Profile ..................................................................................................................3 3
4.2 .4 U nderstand C urrent I&T -R elated Issues .................................................................................................3 3
4.2 .5 C onclusion ..........................................................................................................................................3 3
4.3  S tep 2 : D eterm ine the Initial S cope of the G overnance S ystem ......................................................................3 3
4.3 .1 T ranslating D esign F actors into G overnance and M anagem ent Priorities ..................................................3 4
4.3 .2  C onsider E nterprise S trategy (D esign F actor 1) ......................................................................................3 4
4.3 .3  C onsider E nterprise G oals and A pply the C OB IT  G oals C ascade (D esign F actor 2 ) ...................................3 5
4.3 .4 C onsider the R isk Profile of the E nterprise (D esign F actor 3 ) ..................................................................3 6
4.3 .5 C onsider C urrent I&T -R elated Issues of the E nterprise (D esign F actor 4) .................................................3 6
4.3 .6 C onclusion ..........................................................................................................................................3 6
4.4 S tep 3 : R efine the S cope of the G overnance S ystem ......................................................................................3 7
4.4.1 C onsider the T hreat L andscape (D esign F actor 5) ...................................................................................3 7
4.4.2  C onsider C om pliance R equirem ents (D esign F actor 6) ............................................................................3 8
4.4.3  C onsider the R ole of IT  (D esign F actor 7) ..............................................................................................3 8
4.4.4 C onsider the S ourcing M odel for IT  (D esign F actor 8) ............................................................................3 9
4.4.5 C onsider IT  Im plem entation M ethods (D esign F actor 9 ) .........................................................................3 9
4.4.6 C onsider the T echnology A doption S trategy (D esign F actor 10) ...............................................................40
4.4.7 C onsider E nterprise S ize (D esign F actor 11) ..........................................................................................41
4.4.8 C onclusion ..........................................................................................................................................41
4.5 S tep 4:   R esolve C onflicts and C onclude the G overnance S ystem  D esign .......................................................41
4.5.1 R esolve Inherent Priority C onflicts ........................................................................................................42
4.5.1.1  Purpose .....................................................................................................................................42
4.5.1.2   R esolution S trategies .................................................................................................................42
4.5.1.3   R esolution A pproach ..................................................................................................................43

# T A B LE  O F C O N TE N TS

7

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

4.5.2  C onclude the G overnance S ystem  D esign ...............................................................................................43
4.5.2 .1  C oncluding the D esign ...............................................................................................................43
4.5.2 .2   S ustaining the G overnance S ystem ..............................................................................................44
C hapter 5 . C onnecting W ith the CO BIT ® 2019 Im plem entation G uid e ................4 5
5.1 Purpose of the C O B IT ® 2019 Im plem entation G uide .....................................................................................45
5.2  C OB IT  Im plem entation A pproach .................................................................................................................45
5.2 .1 Phase 1— W hat A re the D rivers? ...........................................................................................................46
5.2 .2  Phase 2 — W here A re W e N ow ? ..............................................................................................................46
5.2 .3  Phase 3 — W here D o W e W ant to B e? .....................................................................................................47
5.2 .4 Phase 4— W hat N eeds to B e D one? .......................................................................................................47
5.2 .5 Phase 5— H ow  D o W e G et T here? .........................................................................................................47
5.2 .6 Phase 6— D id W e G et T here? ................................................................................................................47
5.2 .7 Phase 7— H ow  D o W e K eep the M om entum  G oing? ................................................................................47
5.3  R elationship B etw een C O B IT D esign G uide and C O B IT Im plem entation G uide .............................................47
P art II. Execution and Exam ples ...................................................................................................5 1
C hapter 6 . T he G overnance S ystem  D esign Toolkit .................................................5 1
6.1 Introduction .................................................................................................................................................51
6.2  T oolkit B asics ..............................................................................................................................................51
6.3  S tep 1 and S tep 2 : D eterm ine the Initial S cope of the G overnance S ystem .....................................................52
6.3 .1 E nterprise S trategy (D esign F actor 1) ....................................................................................................52
6.3 .2  E nterprise G oals and A pplying the C OB IT  G oals C ascade (D esign F actor 2 ) ............................................53
6.3 .3  R isk Profile of the E nterprise (D esign F actor 3 ) .....................................................................................54
6.3 .4 C urrent I&T -R elated Issues of the E nterprise (D esign F actor 4) ...............................................................55
6.3 .5 C onclusion ..........................................................................................................................................56
6.4 S tep 3 : R efine the S cope of the G overnance S ystem ......................................................................................58
6.4.1 T hreat L andscape (D esign F actor 5) ......................................................................................................59
6.4.2  C om pliance R equirem ents (D esign F actor 6) ..........................................................................................60
6.4.3  R ole of IT  (D esign F actor 7) .................................................................................................................61
6.4.4 S ourcing M odel for IT  (D esign F actor 8) ...............................................................................................62
6.4.5 IT  Im plem entation M ethods (D esign F actor 9 ) .......................................................................................63
6.4.6 T echnology A doption S trategy (D esign F actor 10) ..................................................................................64
6.4.7 E nterprise S ize (D esign F actor 11) ........................................................................................................65
6.4.8 C onclusion ..........................................................................................................................................65
C hapter 7 . Exam ples ................................................................................................................................6 7
7.1 Introduction .................................................................................................................................................67
7.2  E xam ple 1: M anufacturing E nterprise ...........................................................................................................67
7.2 .1 S tep 1: U nderstand the E nterprise C ontext and S trategy ..........................................................................67
7.2 .2  S tep 2 : D eterm ine the Initial S cope of the G overnance S ystem ................................................................71
7.2 .3  S tep 3 : R efine the S cope of the G overnance S ystem ................................................................................80
7.2 .4 S tep 4: C onclude the G overnance S olution D esign ..................................................................................89
7.2 .4.1  G overnance and M anagem ent Objectives .....................................................................................89
7.2 .4.2   Other C om ponents .....................................................................................................................9 1
7.2 .4.3   S pecific F ocus A rea G uidance ....................................................................................................9 1
7.3  E xam ple 2 : M edium -S ized Innovative C om pany ...........................................................................................9 2
7.3 .1 S tep 1: U nderstand the E nterprise C ontext and S trategy ..........................................................................9 2
7.3 .2  S tep 2 : D eterm ine the Initial S cope of the G overnance S ystem ................................................................9 6
7.3 .3  S tep 3 : R efine the S cope of the G overnance S ystem ..............................................................................105
7.3 .4 S tep 4: C onclude the G overnance S olution D esign ................................................................................115
7.3 .4.1  G overnance and M anagem ent Objectives ...................................................................................115
7.3 .4.2   Other C om ponents ...................................................................................................................117
7.3 .4.3   S pecific F ocus A rea G uidance ...................................................................................................118
7.4 E xam ple 3 : H igh-Profile G overnm ent A gency .............................................................................................118
7.4.1 S tep 1: U nderstand the E nterprise C ontext and S trategy ........................................................................119
7.4.2  S tep 2 : D eterm ine the Initial S cope of the G overnance S ystem ..............................................................12 3
8

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

7.4.3  S tep 3 : R efine the S cope of the G overnance S ystem ..............................................................................13 1
7.4.4 S tep 4: C onclude the G overnance S olution D esign ................................................................................13 2
7.4.4.1  G overnance and M anagem ent Objectives ...................................................................................13 2
7.4.4.2   Other C om ponents ...................................................................................................................13 4
7.4.4.3   S pecific F ocus A rea G uidance ...................................................................................................13 5
A ppendices ......................................................................................................................................................1 37
A ppendix A : M apping T able— E nterprise S trategies to G overnance and M anagem ent Objectives .......................13 7
A ppendix B : M apping T able— E nterprise G oals to A lignm ent G oals .................................................................13 9
A ppendix C : M apping T able— A lignm ent G oals to G overnance and M anagem ent Objectives .............................140
A ppendix D : M apping T able— IT  R isk to G overnance and M anagem ent Objectives ...........................................141
A ppendix E : M apping T able— IT -R elated Issues to G overnance and M anagem ent Objectives ............................143
A ppendix F : M apping T able— T hreat L andscape to G overnance and M anagem ent Objectives ............................145
A ppendix G : M apping T able— C om pliance R equirem ents to G overnance and M anagem ent Objectives ..............146
A ppendix H : M apping T able— R ole of IT  to G overnance and M anagem ent Objectives ......................................147
A ppendix I: M apping T able— S ourcing M odel for IT  to G overnance and M anagem ent Objectives .....................148
A ppendix J:  M apping T able— IT  Im plem entation M ethods to G overnance and M anagem ent Objectives ............149
A ppendix K : M apping T able— T echnology A doption S trategies to G overnance and M anagem ent Objectives ......150

# T A B LE  O F C O N TE N TS

9

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

P age intentionally left blank
10

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# LIST O F FIG U R ES

P art I.  D esign P rocess
C hapter 2 . B asic C oncepts: G overnance System  and C om ponents
F igure 2 .1— C OB IT  Overview ...........................................................................................................................................................17
F igure 2 .2 — C OB IT  C ore M odel ........................................................................................................................................................19
F igure 2 .3 — C apability Levels for Processes ......................................................................................................................................2 1
F igure 2 .4— C OB IT  D esign F actors ...................................................................................................................................................2 2
F igure 2 .5— E nterprise Strategy D esign F actor ..................................................................................................................................2 2
F igure 2 .6— E nterprise G oals D esign F actor ......................................................................................................................................2 2
F igure 2 .7— R isk Profile D esign F actor (IT  R isk C ategories) ............................................................................................................2 3
F igure 2 .8— I&T -R elated Issues D esign F actor ..................................................................................................................................2 6
F igure 2 .9 — T hreat Landscape D esign F actor ....................................................................................................................................2 6
F igure 2 .10— C om pliance R equirem ents D esign F actor ....................................................................................................................2 7
F igure 2 .11— R ole of IT  D esign F actor ..............................................................................................................................................2 7
F igure 2 .12 — Sourcing M odel for IT  D esign F actor ..........................................................................................................................2 7
F igure 2 .13 — IT  Im plem entation M ethods D esign F actor ..................................................................................................................2 7
F igure 2 .14— T echnology A doption Strategy D esign F actor ..............................................................................................................2 8
F igure 2 .15— E nterprise Size D esign F actor ......................................................................................................................................2 8
C hapter 3 . Im pact of D esign Factors
F igure 3 .1— Im pact of D esign F actors on G overnance System ..........................................................................................................2 9
C hapter 4 . D esigning a Tailored G overnance System
F igure 4.1— G overnance System  D esign W orkflow ...........................................................................................................................3 1
F igure 4.2 — G overnance and M anagem ent Objectives Priority M apped to E nterprise Strategy D esign F actor ...............................3 4
F igure 4.3 — G overnance and M anagem ent Objectives Priority M apped to T hreat Landscape D esign F actor ..................................3 7
F igure 4.4— G overnance and M anagem ent Objectives Priority M apped to C om pliance R equirem ents D esign F actor ....................3 8
F igure 4.5— G overnance and M anagem ent Objectives Priority M apped to R ole of IT  D esign F actor ..............................................3 8
F igure 4.6— G overnance and M anagem ent Objectives Priority M apped to Sourcing M odel for IT  D esign F actor ..........................3 9
F igure 4.7— G overnance and M anagem ent Objectives Priority M apped to IT  Im plem entation M ethods D esign F actor .................40
F igure 4.8— G overnance and M anagem ent Objectives Priority M apped to T echnology A doption Strategy D esign F actor .............40
F igure 4.9 — G overnance and M anagem ent Objectives Priority M apped to E nterprise Size D esign F actor ......................................41
F igure 4.10— G overnance System  D esign Step 4— C onclusion ........................................................................................................42
C hapter 5 . C onnecting W ith the C O B IT® 20 1 9 Im plem entation G uide
F igure 5.1— C OB IT  Im plem entation R oadm ap ..................................................................................................................................46
F igure 5.2 — C onnection Points B etw een C OB IT  D esign G uide and C OB IT  Im plem entation G uide ...............................................48

## P art II. Execution and Exam ples

C hapter 7 . Exam ples
F igure 7.1— E xam ple 1, Step 1.1: E nterprise Strategy .......................................................................................................................67
F igure 7.2 — E xam ple 1, Step 1.2 : E nterprise G oals ...........................................................................................................................68
F igure 7.3 — E xam ple 1, Step 1.3 : R isk Profile ...................................................................................................................................69
F igure 7.4— E xam ple 1, Step 1.4: I&T -R elated Issues .......................................................................................................................70
F igure 7.5— E xam ple 1, Step 2 .1: E nterprise Strategy .......................................................................................................................71
F igure 7.6— E xam ple 1, Step 2 .1: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 1
E nterprise Strategy .........................................................................................................................................................72
F igure 7.7— E xam ple 1, Step 2 .2 : E nterprise G oals ...........................................................................................................................73
F igure 7.8— E xam ple 1, Step 2 .2 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 2
E nterprise G oals .............................................................................................................................................................74
F igure 7.9 — E xam ple 1, Step 2 .3 : R isk Profile ...................................................................................................................................75

# LIST O F FIG U R E S

11

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

F igure 7.10— E xam ple 1, Step 2 .3 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 3  R isk Profile 76
F igure 7.11— E xam ple 1, Step 2 .4: I&T -R elated Issues .....................................................................................................................77
F igure 7.12 — E xam ple 1, Step 2 .4: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 4
I&T -R elated Issues .......................................................................................................................................................78
F igure 7.13 — E xam ple 1, Step 2 .5: Initial D esign Sum m ary of G overnance and M anagem ent Objectives Im portance ...................79
F igure 7.14— E xam ple 1 T ailored Version of G overnance System ....................................................................................................80
F igure 7.15— E xam ple 1, Step 3 .1: T hreat Landscape .......................................................................................................................82
F igure 7.16— E xam ple 1, Step 3 .1: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 5
T hreat Landscape ..........................................................................................................................................................82
F igure 7.17— E xam ple 1, Step 3 .2 : C om pliance R equirem ents .........................................................................................................83
F igure 7.18— E xam ple 1, Step 3 .2 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 6
C om pliance R equirem ents ............................................................................................................................................84
F igure 7.19 — E xam ple 1, Step 3 .3 : R ole of IT ...................................................................................................................................84
F igure 7.2 0— E xam ple 1, Step 3 .3 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 7 R ole of IT ...85
F igure 7.2 1— E xam ple 1, Step 3 .4: Sourcing M odel for IT ...............................................................................................................86
F igure 7.2 2 — E xam ple 1, Step 3 .4: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 8
Sourcing M odel for IT ..................................................................................................................................................86
F igure 7.2 3 — E xam ple 1, Step 3 .5: IT  Im plem entation M ethods .......................................................................................................87
F igure 7.2 4— E xam ple 1, Step 3 .5: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 9
IT  Im plem entation M ethods .........................................................................................................................................87
F igure 7.2 5— E xam ple 1, Step 3 .6: T echnology A doption  Strategy ..................................................................................................88
F igure 7.2 6— E xam ple 1, Step 3 .6: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 10
T echnology A doption Strategy .....................................................................................................................................88
F igure 7.2 7— E xam ple 1, Step 4: G overnance and M anagem ent Objectives Im portance (A ll D esign F actors) ................................89
F igure 7.2 8— E xam ple 1, G overnance and M anagem ent Objectives and T arget Process C apability Levels .....................................9 0
F igure 7.2 9 — E xam ple 2 , Step 1.1: E nterprise Strategy .....................................................................................................................9 2
F igure 7.3 0— E xam ple 2 , Step 1.2 : E nterprise G oals .........................................................................................................................9 3
F igure 7.3 1— E xam ple 2 , Step 1.3 : R isk Profile .................................................................................................................................9 4
F igure 7.3 2 — E xam ple 2 , Step 1.4: I&T -R elated Issues .....................................................................................................................9 5
F igure 7.3 3 — E xam ple 2 , Step 2 .1: E nterprise Strategy .....................................................................................................................9 6
F igure 7.3 4— E xam ple 2 , Step 2 .1: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 1
E nterprise Strategy .......................................................................................................................................................9 7
F igure 7.3 5— E xam ple 2 , Step 2 .2 : E nterprise G oals .........................................................................................................................9 8
F igure 7.3 6— E xam ple 2 , Step 2 .2 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 2
E nterprise G oals ...........................................................................................................................................................9 9
F igure 7.3 7— E xam ple 2 , Step 2 .3 : R isk Profile ...............................................................................................................................100
F igure 7.3 8— E xam ple 2 , Step 2 .3 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 3  R isk Profile .......101
F igure 7.3 9 — E xam ple 2 , Step 2 .4: I&T -R elated Issues ...................................................................................................................102
F igure 7.40— E xam ple 2 , Step 2 .4: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 4
I&T -R elated Issues .....................................................................................................................................................103
F igure 7.41— E xam ple 2 , Step 2 .5: Initial D esign Sum m ary of G overnance and M anagem ent Objectives Im portance .................104
F igure 7.42 — G overnance System  Scope R efinem ent T able A pplied to E xam ple 2 ........................................................................105
F igure 7.43 — E xam ple 2 , Step 3 .1: T hreat Landscape .....................................................................................................................107
F igure 7.44— E xam ple 2 , Step 3 .1: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 5
T hreat Landscape ........................................................................................................................................................107
F igure 7.45— E xam ple 2 , Step 3 .2 : C om pliance R equirem ents .......................................................................................................109
F igure 7.46— E xam ple 2 , Step 3 .2 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 6
C om pliance R equirem ents ..........................................................................................................................................109
F igure 7.47— E xam ple 2 , Step 3 .3 : R ole of IT .................................................................................................................................110
F igure 7.48— E xam ple 2 , Step 3 .3 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 7 R ole of IT .110
F igure 7.49 — E xam ple 2 , Step 3 .4: Sourcing M odel for IT ..............................................................................................................112
F igure 7.50— E xam ple 2 , Step 3 .4: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 8
Sourcing M odel for IT ................................................................................................................................................112
F igure 7.51— E xam ple 2 , Step 3 .5: IT  Im plem entation M ethods .....................................................................................................113
F igure 7.52 — E xam ple 2 , Step 3 .5: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 9
IT  Im plem entation M ethods .......................................................................................................................................113
F igure 7.53 — E xam ple 2 , Step 3 .6: T echnology A doption Strategy .................................................................................................114
F igure 7.54— E xam ple 2 , Step 3 .6: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 10
T echnology A doption Strategy ...................................................................................................................................114
12

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

F igure 7.55— E xam ple 2 , Step 4.1: G overnance and M anagem ent Objectives Im portance (A ll D esign F actors) ...........................115
F igure 7.56— E xam ple 2  G overnance and M anagem ent Objectives w ith T arget Process C apability Levels ..................................116
F igure 7.57— E xam ple 3 , Step 1.1: E nterprise Strategy ...................................................................................................................119
F igure 7.58— E xam ple 3 , Step 1.2 : E nterprise G oals .......................................................................................................................12 0
F igure 7.59 — E xam ple 3 , Step 1.3 : R isk Profile ...............................................................................................................................12 1
F igure 7.60— E xam ple 3 , Step 1.4: I&T -R elated Issues ...................................................................................................................12 2
F igure 7.61— E xam ple 3 , Step 2 .1: E nterprise Strategy ...................................................................................................................12 3
F igure 7.62 — E xam ple 3 , Step 2 .1: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 1
E nterprise Strategy .....................................................................................................................................................12 3
F igure 7.63 — E xam ple 3 , Step 2 .2 : E nterprise G oals .......................................................................................................................12 4
F igure 7.64— E xam ple 3 , Step 2 .2 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 2
E nterprise G oals .........................................................................................................................................................12 5
F igure 7.65— E xam ple 3 , Step 2 .3 : R isk Profile ...............................................................................................................................12 6
F igure 7.66— E xam ple 3 , Step 2 .3 : R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 3
R isk Profile .................................................................................................................................................................12 7
F igure 7.67— E xam ple 3 , Step 2 .4: I&T -R elated Issues ...................................................................................................................12 8
F igure 7.68— E xam ple 3 , Step 2 .4: R esulting G overnance/M anagem ent Objectives Im portance for D esign F actor 4
I&T -R elated Issues .....................................................................................................................................................12 9
F igure 7.69 — E xam ple 3 , Step 2 .5: Initial D esign Sum m ary of G overnance and M anagem ent Objectives Im portance .................13 0
F igure 7.70— G overnance System  Scope R efinem ent T able A pplied to E xam ple 3 ........................................................................13 1
F igure 7.71— E xam ple 3 , Step 4: G overnance and M anagem ent Objectives Im portance (A ll D esign F actors) ..............................13 2
F igure 7.72 — E xam ple 3  G overnance and M anagem ent Objectives and T arget Process C apability Levels ....................................13 3
F igure 7.73 — E xam ple 3 , Step 4: Organizational Structures ............................................................................................................13 5
A ppendices ..........................................................................................................................................................................13 7
F igure A .1— M apping E nterprise Strategies to G overnance and M anagem ent Objectives ..............................................................13 7
F igure A .2 — M apping E nterprise G oals to A lignm ent G oals ...........................................................................................................13 9
F igure A .3 — M apping A lignm ent G oals to G overnance and M anagem ent Objectives ....................................................................140
F igure A .4— M apping IT  R isk to G overnance and M anagem ent Objectives ...................................................................................141
F igure A .5— M apping I&T -R elated Issues to G overnance and M anagem ent Objectives ................................................................143
F igure A .6— M apping T hreat Landscape to G overnance and M anagem ent Objectives ..................................................................145
F igure A .7— M apping C om pliance R equirem ents to G overnance and M anagem ent Objectives ....................................................146
F igure A .8— M apping R ole of IT  to G overnance and M anagem ent Objectives ..............................................................................147
F igure A .9 — M apping Sourcing M odel for IT  to G overnance and M anagem ent Objectives ...........................................................148
F igure A .10— M apping IT  Im plem entation M ethods to G overnance and M anagem ent Objectives ................................................149
F igure A .11— M apping T echnology A doption Strategy to G overnance and M anagem ent Objectives ............................................150

# LIST O F FIG U R E S

13

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

P age intentionally left blank
14

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

15

# C H A P TE R  1

# IN TR O DU C TIO N  A N D P U R P O SE

P art I
Design P rocess
C hapter 1

## Introduction and P urpose

1.1  G overnance System s
T his publication describes how  an enterprise can design a custom ized governance solution for enterprise inform ation and
technology (I&T ). A n effective and efficient governance system  over I&T  is the starting point for generating value. T his
applies to all types and sizes of enterprises. G overnance over a com plex dom ain like I&T  requires a m ultitude of
com ponents, including processes, organizational structures, inform ation flow s and behaviors. A ll of these elem ents m ust
w ork together in a system ic w ay; therefore, this publication refers to the tailored governance solution that every enterprise
should build as the “governance system  for enterprise I&T ,” or “governance system ” for short.
T here is no unique, one-size-fits-all governance system  for enterprise I&T . E very enterprise has its ow n distinct
character and profile, and w ill differ from  other organizations in several critical respects: size of the enterprise,
industry sector, regulatory landscape, threat landscape, role of IT  for the organization and tactical technology-related
choices, am ong others. A ll of these aspects— to w hich C OB IT ® refers, collectively, as design factors— require
organizations to tailor their governance system s to realize the m ost value out of their use of I&T .
T ailoring m eans that an enterprise should start from  the C OB IT ® core m odel, and from  there, apply changes to the
generic fram ew ork based on the relevance and im portance of a series of design factors. T his process is called
“designing the governance system  for enterprise I&T .”
1.2   Structure of This P ublication
T his publication contains the follow ing m ajor parts, chapters and appendices:

## Part I: D esign Process

C hapter 1 provides an introduction denoting the structure and intended audience. 
C hapter 2  review s key concepts and definitions from  the C O BIT ® 2019 Fram ew ork: Introduction and 
M ethodology publication, including the design factor concept.
C hapter 3  explores the im plications of design factors on the design of the governance solution. 
C hapter 4 is the core of the publication. It presents a w orkflow  for designing an enterprise governance solution, 
taking into account all potential design factors. T he w orkflow  consists of four distinct steps, and results in a
tailored governance solution.
C hapter 5 explains how  this publication relates to the C O BIT ® 2019 Im plem entation G uide, and how  the tw o 
should be used together.
Part II: E xecution and E xam ples
C hapter 6 introduces the C O BIT ® 2019 D esign G uide toolkit— an E xcel ® tool that facilitates the governance 
system  design w orkflow .
C hapter 7 illustrates how  the w orkflow  of C hapter 4 m ay be applied, using the tool. 
A ppendices A  through K  contain various m apping tables used during the design process. 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

16
1.3  T arget A udience for This P ublication
T he target audience for this publication includes a range of direct stakeholders in governance over I&T : board
m em bers, executive and senior m anagem ent, and experienced professionals throughout the enterprise, not only from
the business and IT , but also from  audit, assurance, com pliance, security, privacy and risk m anagem ent disciplines.
Other indirect stakeholders in governance over I&T  include custom ers, users and citizens; they constitute the m ost
im portant beneficiaries of good governance, even though m ost w ill rarely turn to this publication. T heir interests are
assum ed by the direct stakeholders m entioned previously.
A  certain level of experience and a thorough understanding of the enterprise are required to benefit from  this guide.
Such experience and understanding allow  users to custom ize core C OB IT ® 2 019  guidance— w hich is generic in
nature— into tailored and focused guidance for the enterprise, taking into account the enterprise’s context.
T he target audience includes those responsible during the w hole life cycle of the governance solution, from  initial
design, to execution and assurance. Indeed, assurance providers m ay apply the logic and w orkflow  developed in this
publication to create a w ell-substantiated assurance program  for the enterprise.
1.4  R elated G uidance: C O B IT ® 2019 Im plem entation G uide
T he C O BIT ® 2019 Im plem entation G uide is related to this publication. It describes the road m ap for continuously
im proving governance over enterprise I&T . T he (initial) design of such a governance system , w hich is described
herein, is part of the initial phases of that road m ap.
C hapter 5 of this guide elaborates on the links betw een the tw o publications, and illustrates how  to use them  together.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

17

# C H A P TE R  2

B A SIC  C O N C E P TS: G O V E R N A N C E  SYSTE M  A N D C O M P O N E N TS
C hapter 2
Basic C oncepts: G overnance S ystem  and C om ponents
2.1  Introduction
Figure 2.1 show s the high-level overview  of C OB IT ® 2 019 , and how  the different publications cover different
aspects.

C OB IT ® 2 019  is based on C OB IT ® 5 and other authoritative sources. C OB IT  is aligned to a num ber of related
standards and fram ew orks. T he list of these standards is included in C hapter 10 of C O BIT ® 2019 Fram ew ork:
Introduction and M ethodology. T he analysis of related standards and C OB IT ’s alignm ent to them  underly C OB IT ’s
established position of being the um brella I&T  governance fram ew ork.
In the future, C OB IT  w ill call upon its user com m unity to propose content updates, to be applied as controlled
contributions on a continuous basis, to keep C OB IT  up to date w ith the latest insights and evolutions.
T he C OB IT  product fam ily is open-ended. A t the tim e of publication of this guide, the follow ing publications are
available:
C O B IT ® 2019 F ram ew ork: Introduction and M ethodology introduces the key concepts of C OB IT ® 2 019 . 
C O B IT ® 2019 F ram ew ork: G overnance and M anagem ent O bjectives com prehensively describes the 40 core 
governance and m anagem ent objectives, the processes contained therein, and other related com ponents. T his guide
also references other standards and fram ew orks.

## Figure 2.1— C O BIT O verview

• Enterprise str ategy
• Enterprise goals
• Enterprise siz e

## • Role of I T

• Sour cing model for I T
• Compliance r equir ements
• Etc.

# • SME

• Security
• Risk
• De vOps
• Etc.
➢ Priority go vernance
a n d  m a n a g e m e n t
o b j e c t i v e s
➢ Specific guidance
from focus areas
➢ Target capability
a n d  p e r f o r m a n c e
m a n a g e m e n t
g u i d a n c e
Design F act ors

# COBIT 5

Inputs to COBIT®  2019 COBIT®  2019
Community
Contribution
Standards,
Frameworks,
Regulations

## COBI T Core

Publications

## Focus Area

## Tailored Enterprise

Governance

## System for

## Information and

Technology

## COBIT Core

## Reference Model of Governance

## and Management Objectives

COBI T®  2019 F ramework:

## Intr oduction and Methodology

COBI T®  2019 F ramework:

## Governance and

Management Objectiv es

## COBI T®  2019 Design Guide:

## Designing an Information and Technology

## Governance Solution

## COBI T®  2019 Implementation Guide:

## Implementing and Optimizing an

## Information and Technology

## Governance Solution

## EDM01— Ensured

Governance

## Framework Setting

## and Maintenance

## APO01— Managed

## I&T Management

Framework

## APO08— Managed

Relationships

## APO02— Managed

Strategy

## APO09— Managed

Service
Agreements

## APO03— Managed

Enterprise
Architecture

## APO10— Managed

Vendors

## APO04— Managed

Innovation

## APO11— Managed

Quality

## APO05— Managed

Portfolio

## APO12— Managed

Risk

## APO06— Managed

## Budget and Costs

## APO07— Managed

## Human Resources

## APO14— Managed

Data

## MEA01— Managed

## Performance and

Conformance
Monitoring

## MEA02— Managed

## System of Internal

Control

## MEA03— Managed

## Compliance with

External
Requirements
MEA04— Manag ed
Assu rance

## APO13— Managed

Security
DSS01 — Manag ed
Oper atio ns
DSS02 — Manag ed
Ser vice Req uests

## and Incidents

DSS03 — Manag ed
Problems
DSS04 — Manag ed
Continuity
DSS05 — Manag ed
Security
Ser vices
DSS06 — Manag ed
Business

## Process Controls

## BAI01— Managed

Programs

## BAI08— Managed

Knowledge

## BAI02— Managed

Requirements
Definition

## BAI09— Managed

Assets

## BAI03— Manage

Solutions
Identification

## and Build

## BAI10— Managed

Configuration

## BAI04— Managed

Availability

## and Capacity

## BAI11— Managed

Projects

## BAI05— Managed

Organizational
Change

## BAI06— Managed

## IT Changes

## BAI07— Managed

## IT Change

## Acceptance and

Transitioning

## EDM02— Ensured

## Benefits Delivery

## EDM03— Ensured

## Risk Optimization

## EDM04— Ensured

Resource
Optimization

## EDM05— Ensured

Stakeholder
Engagement

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

18
C O B IT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution explores design 
factors that can influence governance and includes a w orkflow  for planning a tailored governance system  for the
enterprise.
C O B IT ® 2019 Im plem entation G uide: Im plem enting and O ptim izing an Inform ation and Technology 
G overnance Solution represents an evolution of the C O BIT ® 5 Im plem entation guide and develops a road m ap for
continuous governance im provem ent. It m ay be used in com bination w ith the C O BIT ® 2019 D esign G uide .
T he content identified as focus areas in figure 2.1 w ill contain m ore detailed guidance on specific them es. A  num ber
of these focus area content guides are already in preparation; others are planned. T he set of focus area guides is open-
ended and w ill continue to evolve. F or the latest inform ation on currently available and planned publications and
other content, please visit w w w.isaca.org/cobit .
T he rem ainder of this section describes the basic concepts of C OB IT ® 2 019  as they are defined in the C OB IT
fram ew ork publications. T he design factors, focus areas and variants concepts w ill be used to design a tailored
governance system  for enterprise I&T .  A  tailored governance system  based on C OB IT  is a system  that has taken the
generic contents of C OB IT  and has assigned specific priorities and target capability levels to the governance and
m anagem ent com ponents based on the enterprise’s ow n context and design factor values. W hen required, specific
variants of governance com ponents are also put in place.
2.2   G overnance and M anagem ent O bjectives
F or inform ation and technology to contribute to enterprise goals, a num ber of governance and m anagem ent
objectives should be achieved.  B asic concepts relating to governance and m anagem ent objectives are:
A  governance or m anagem ent objective alw ays relates to one process (w ith an identical or sim ilar nam e) and a 
series of related com ponents of other types to help achieve the objective.
A  governance objective relates to a governance process (depicted in the dark blue background in figure 2.2 ), w hile 
a m anagem ent objective relates to a m anagem ent process (depicted on the lighter blue background in figure 2.2 ).
B oards and executive m anagem ent are typically accountable for governance processes, w hile m anagem ent
processes are the dom ain of senior and m iddle m anagem ent.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

19

# C H A P TE R  2

B A SIC  C O N C E P TS: G O V E R N A N C E  SYSTE M  A N D C O M P O N E N TS

T he governance and m anagem ent objectives in C OB IT  are grouped into five dom ains. T he dom ains have nam es w ith
verbs that express the key purpose and areas of activity of the objective contained in them :
G overnance objectives are grouped in the E valuate, D irect and M onitor (E D M ) dom ain. In this dom ain, the 
governing body evaluates strategic options, directs senior m anagem ent on the chosen strategic options and
m onitors the achievem ent of the strategy.
M anagem ent objectives are grouped in four dom ains: 
A lign, Plan and O rganize (A PO) addresses the overall organization, strategy and supporting activities for I&T . 
Build, A cquire and Im plem ent (B A I) treats the definition, acquisition and im plem entation of I&T  solutions and 
their integration in business processes.
Deliver, Service and Support (D SS) addresses the operational delivery and support of I&T  services, including 
security.
Monitor, E valuate and A ssess (M E A ) addresses perform ance m onitoring and conform ance of I&T  w ith internal 
perform ance targets, internal control objectives and external requirem ents.
Figure 2.2— C O BIT C ore M odel
EDM01 — Ensur ed
Governance

## Framework Setting

## and Maintenance

APO01 — Managed

## I&T Management

Framework
APO08 — Managed
Relationships
APO02 — Managed
Strategy
APO09 — Managed
Service
Agr eements
APO03 — Managed
Enterprise
Architecture
APO10 — Managed
Vendors
APO04 — Managed
Inno vation
APO11 — Managed
Quality
APO05 — Managed
Portfolio
APO12 — Managed
Risk
APO 06— Managed

## Budget and Costs

APO 07— Managed

## Human Resources

APO 14— Managed
Data
MEA01 — Managed

## Performance and

Conformance
Monit oring
MEA02 — Managed

## System of Internal

Contr ol

## MEA03— Managed

## Compliance With

External
Requirements

## MEA04— Managed

Assur ance
APO 13— Managed
Security
DSS01 — Managed
Oper ations
DSS02 — Managed

## Service Requests

## and Incidents

DSS03 — Managed
Problems
DSS04 — Managed
Continuity
DSS05 — Managed
Security
Services
DSS06 — Managed
Business

## Process Controls

BAI 01— Managed
Programs
BAI 08— Managed
Knowledge
BAI 02— Managed
Requirements
Definition
BAI 09— Managed
Assets
BAI 03— Managed
Solutions
Identification

## and Build

BAI 10— Managed
Configur ation
BAI 04— Managed
Availability

## and Capacity

BAI 11— Managed
Projects
BAI 05— Managed
Organizational
Change
BAI 06— Managed

## IT Changes

BAI 07— Managed

## IT Change

## Acceptance and

Transitioning
EDM02 — Ensur ed
Benefits Deliv ery
EDM03 — Ensur ed

## Risk Optimization

EDM04 — Ensur ed
Resource
Optimization
EDM05 — Ensur ed
Stakeholder
Engagement

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

20
2.3  C om ponents of the G overnance System
T o satisfy governance and m anagem ent objectives, each enterprise needs to establish, tailor and sustain a governance
system  built from  a num ber of com ponents.
C om ponents are factors that, individually and collectively, contribute to the good operations of the enterprise’s 
governance system  over I&T .
C om ponents interact w ith each other, resulting in a holistic governance system  for I&T . 
C om ponents can be of different types. T he m ost fam iliar are processes. H ow ever, com ponents of a governance 
system  also include organizational structures; policies and procedures; inform ation item s; culture and behavior;
skills and com petencies; and services, infrastructure and applications.
C om ponents of all types can be generic or can be variants of generic com ponents: 
Generic com ponents are described in the C OB IT  core m odel (see figure 2.2 ) and apply in principle to any 
situation. H ow ever, they are generic in nature and generally need custom ization before being practically
im plem ented.
Variants are based on generic com ponents but are tailored for a specific purpose or context w ithin a focus area 
(e.g., for inform ation security, D evOps, a particular regulation).
2.4  Focus A reas
A  focus area describes a certain governance topic, dom ain or issue that can be addressed by a collection of
governance and m anagem ent objectives and their com ponents. E xam ples of focus areas include: sm all and m edium
enterprises, cybersecurity, digital transform ation, cloud com puting, privacy, and D evOps. 1
1 F ocus areas m ay contain a
com bination of generic governance com ponents and variants.
T he num ber of focus areas is virtually unlim ited. T hat is w hat m akes C OB IT  open-ended. N ew  focus areas can be
added as required or as subject m atter experts and practitioners contribute to the open-ended C OB IT  m odel.
2.5  C apability Levels
C OB IT ® 2 019  supports a C apability M aturity M odel Integration (C M M I ® )-based process capability schem e. T he
process w ithin each governance and m anagem ent objective can operate at various capability levels, ranging from  0
to 5. T he capability level is a m easure for how  w ell a process is im plem ented and perform ing.  Figure 2.3 depicts the
m odel, the increasing capability levels and the general characteristics of each.
1
1 D evOps exem plifies both a com ponent variant and a focus area. W hy?  D evOps is a current them e in the m arketplace and definitely requires specific
guidance, m aking it a focus area. D evOps includes a num ber of generic governance and m anagem ent objectives of the core C OB IT  m odel, along w ith
a num ber of variants of developm ent-, operational- and m onitoring-related processes and organizational structures.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

21

# C H A P TE R  2

B A SIC  C O N C E P TS: G O V E R N A N C E  SYSTE M  A N D C O M P O N E N TS

T he C OB IT  core m odel assigns capability levels to all process activities, allow ing to clearly define processes at
different capability levels.  In this guide w e w ill som etim es refer to ‘low er’ or ‘higher’ capability levels. A s a
convention in this guide, any level at 3  or up is called ‘higher,’ anything below  3  is called ‘low er.’
2.6   Design Factors
D esign factors are factors that can influence the design of an enterprise’s governance system  and position it for
success in the use of I&T . T he design factors are listed below  and their potential im pact on the governance system  is
discussed in C hapter 3 .
D esign factors include any com bination of the follow ing ( figure 2.4 ):
Figure 2.3 — C apability Levels for P rocesses
The pr ocess achie ves its purpose, is well
defined, its per formance is measur ed t o
impr ove performance and continuous
impr ovement is pursued.
The pr ocess achie ves its purpose, is well defined, and its
per formance is (quantitativ ely) measur ed.
The pr ocess achie ves its purpose through the application of a basic, yet complete, set of
activities that can be char acteriz ed as per formed.
The pr ocess mor e or less achie ves its purpose through the application of an incomplete set of activities that
can be char acteriz ed as initial or intuitiv e— not v ery organized.
• Lack of any basic capability
• Incomplete appr oach t o addr ess go vernance and management purpose
• Ma y or ma y not be meeting the intent of any pr ocess pr actices
The pr ocess achie ves its purpose in a much more organized way using
organizational assets. Processes typically are well defined.
0
1
2
3
4
5

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

22

1. E nterprise strategy — E nterprises can have different strategies, w hich can be expressed as one or m ore of the
archetypes show n in figure 2.5 . Organizations typically have a prim ary strategy and, at m ost, one secondary strategy.

2 . E nterprise goals supporting the enterprise strategy— E nterprise strategy is realized by the achievem ent of (a set
of) enterprise goals. T hese goals are defined in the C OB IT  fram ew ork, structured along the balanced scorecard
(B SC ) dim ensions, and include the follow ing ( figure 2.6 ):

2
2 C orresponds w ith prospector in the M iles-Snow  typology. See “M iles and Snow ’s T ypology of D efender, Prospector, A nalyzer, and R eactor,” E library,
https://ebrary.net/3 73 7/m anagem ent/m iles_snow s_typology_defender_prospector_analyzer_reactor .
3
3 See R eeves, M artin; C laire Love, Philipp T illm anns, “Your Strategy N eeds a Strategy,” H arvard Business Review , Septem ber 2 012 ,
https://hbr.org/2012/09/your-strategy-needs-a-strategy , specifically regarding visionary and shaping.
4
4 C orresponds to cost leadership; see U niversity of C am bridge, “Porter’s G eneric C om petitive Strategies (w ays of com peting),” Institute for
M anufacturing (IfM ) M anagem ent T echnology Policy, https://w w w.ifm .eng.cam .ac.uk/research/dstools/porters-generic-com petitive-strategies/ . A lso
corresponds to operational excellence; see T reacy, M ichael; F red W iersem a, “C ustom er Intim acy and Other Value D isciplines,” H arvard Business
Review , January/F ebruary 19 9 3 , https://hbr.org/1993 /01/custom er-intim acy-and-other-value-disciplines .
5
5 C orresponds w ith defenders in the M iles-Snow  typology. See op cit “M iles and Snow ’s T ypology of D efender, Prospector, A nalyzer, and R eactor.”

## Figure 2.4— C O BIT Design Factors

## Future Factors

Enterprise
Str ategy
Enterprise
Goals Risk Profile I&T -Re lated
Issues
Threat
Landscape
Compliance

## Requir ements Role of I T

Sour cing
Model

## for I T

# IT

Impl ementation
Methods
Technology

## Adopti on

Str ate gy
Enterpri se
Size

## Figure 2.5— Enterprise Strategy Design Factor

## Strategy A rchetype Explanation

G row th/A cquisition The enterprise has a focus on growing (revenues) 2
2
Innovation/Differentiation The enterprise has a focus on offering different and/or innovative products
and services to their clients 3
3
C ost Leadership The enterprise has a focus on short-term cost minimization 4
4
C lient Service/Stability The enterprise has a focus on providing a stable and client-oriented service.5
5
Figure 2.6 — Enterprise G oals Design Factor
Reference Balanced Scorecard (BSC )
Dim ension Enterprise G oal
EG 01 Financial Portfolio of competitive products and services
EG 02 Financial Managed business risk
EG 03 Financial Compliance with external laws and regulations
EG 04 Financial Quality of ﬁnancial information

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

23

# C H A P TE R  2

B A SIC  C O N C E P TS: G O V E R N A N C E  SYSTE M  A N D C O M P O N E N TS
3 . R isk profile of the enterprise and current issues in relation to I&T — T he risk profile identifies the sort of IT -
related risk to w hich the enterprise is currently exposed and indicates w hich areas of risk are exceeding the risk
appetite.
T he risk categories listed in figure 2.7 m erit consideration. 6
6

6
6 M odified from  ISA C A , The Risk IT Practitioner G uide , U SA , 2 009
Figure 2.6 — Enterprise G oals Design Factor (cont.)
EG 05 Customer Customer-oriented service culture
EG 06 Customer Business service continuity and availability
EG 07 Customer Quality of management information
EG 08 Internal Optimization of internal business process functionality
EG 09 Internal Optimization of business process costs
EG 10 Internal Staff skills, motivation and productivity
EG 11 Internal Compliance with internal policies
EG 12 Growth Managed digital transformation programs
EG 13 Growth Product and business innovation
Figure 2.7 — R isk P rofile Design Factor (IT R isk C ategories)

## Reference Risk C ategory Exam ple Risk Scenarios

1 IT-investment decision
making, portfolio
deﬁnition and
maintenance
A. Programs selected for implementation misaligned with corporate strategy and
priorities
B. Failure of IT-related Investments to support digital strategy of the enterprise
C. Selection of wrong software (in terms of cost, performance, features, compatibility,
redundancy, etc.) for acquisition and implementation
D. Selection of wrong infrastructure (in terms of cost, performance, features,
compatibility, etc.) for implementation
E. Duplication or important overlaps between different investment initiatives
F. Long-term incompatibility between new investment programs and enterprise
architecture
G. Misallocation, ineﬃcient management and/or competition for resources without
alignment to business priorities
2 Program and projects
lifecycle management
A. Failure of senior management to terminate failing projects (due to cost explosion,
excessive delays, scope creep, changed business priorities)
B. Budget overruns for I&T projects

## C. Lack of quality of I&T projects

D. Late delivery of I&T projects
E. Failure of third-party outsourcers to deliver projects as per contractual agreements
(any combination of exceeded budgets, quality problems, missing functionality,
late delivery)
3 IT cost and oversight A. Extensive dependency on, and use of, user-created, user-deﬁned, user-maintained
applications and ad hoc solutions
B. Excess cost and/or ineffectiveness of I&T-related purchases outside of the I&T
procurement process
C. Inadequate requirements leading to ineffective Service Level Agreements (SLAs)
D. Lack of funds for I&T related investments
4 IT expertise, skills and
behavior
A. Lack or mismatch of IT-related skills within IT (e.g., due to new technologies or
working methods)
B.Lack of business understanding by IT staff that affects service delivery/project quality
C. Inability to recruit and retain IT staff
D. Recruitment of unsuitable proﬁles because of lack of due diligence in the recruitment
process

## E. Lack of I&T training

F. Overreliance for I&T services on key staff

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

24
Figure 2.7 — R isk P rofile Design Factor (IT R isk C ategories) (cont.)

## Reference Risk C ategory Exam ple Risk Scenarios

5 Enterprise/IT
architecture
A. Complex, inﬂexible enterprise architecture (EA), obstructing further evolution and
expansion, and leading to missed business opportunities
B. Failure to timely adopt and exploit new infrastructure or abandon obsolete
infrastructure
C. Failure to timely adopt and exploit new software (functionality, optimization, etc.)
or to abandon obsolete applications
D. Undocumented EA leading to ineﬃciencies and duplications
E. Excessive number of exceptions on enterprise architecture standards
6 IT operational
infrastructure incidents
A. Accidental damaging of IT equipment
B. Errors by IT staff (during backup, during upgrades of systems, during maintenance
of systems, etc.)
C. Incorrect information input by IT staff or system users
D. Destruction of data center (sabotage, etc.) by staff
E. Theft of device with sensitive data
F. Theft of a key infrastructure component
G. Erroneous conﬁguration of hardware components
H. Intentional tampering with hardware (security devices, etc.)
I. Abuse of access rights from prior roles to access IT infrastructure
J. Loss of backup media or backups not checked for effectiveness
K. Loss of data by cloud provider
L. Operational-service interruption by cloud providers
7 Unauthorized actions A. Tampering with software
B. Intentional modiﬁcation or manipulation of software leading to incorrect data
C. Intentional modiﬁcation or manipulation of software leading to fraudulent actions
D. Unintentional modiﬁcation of software leading to inaccurate results
E. Unintentional conﬁguration and change-management errors
8 Software adoption/
usage problems
A. Nonadoption of new application software by users
B. Ineﬃcient use of new software by users
9 Hardware incidents A. System instability in wake of installing new infrastructure, leading to operational
incidents (e.g., BYOD program)
B. Inability of systems to handle transaction volumes when user volumes increase
C. Inability of systems to handle load when new applications or initiatives are deployed
D. Utilities failure (telecom, electricity)
E. Hardware failure due to overheating and/or other environmental conditions like
humidity
F. Damaging of hardware components leading to destruction of data by internal staff
G. Loss/disclosure of portable media containing sensitive data (CD, USB-drives,
portable disks, etc.)
H. Extended resolution time or support delays in case of hardware incidents
10 Software failures A. Inability to use the software to realize desired outcomes (e.g., failure to make
required business model or organizational changes)
B. Implementation of immature software (early adopters, bugs, etc.)
C. Operational glitches when new software is made operational
D. Regular software malfunctioning of critical application software
E. Obsolete application software (outdated, poorly documented, expensive to
maintain, diﬃcult to extend, not integrated in current architecture, etc.)
F. Inability to revert back to former versions in case of operational issues with a new
version
G. Software-induced corrupted data(base) leading to inaccessible data

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

25

# C H A P TE R  2

B A SIC  C O N C E P TS: G O V E R N A N C E  SYSTE M  A N D C O M P O N E N TS
Figure 2.7 — R isk P rofile Design Factor (IT R isk C ategories) (cont.)

## Reference Risk C ategory Exam ple Risk Scenarios

11 Logical attacks
(hacking, malware,
etc.)
A. Unauthorized (internal) users trying to break into systems
B. Service interruption due to denial-of-service (DoS) attack
C. Website defacement
D. Malware attack
E. Industrial espionage

## F. Hacktivism

G. Disgruntled employee implements a time bomb which leads to data loss
H. Company data stolen through unauthorized access gained by a phishing attack
I. Foreign government attacks on critical systems
12 Third-party/supplier
incidents
A. Inadequate performance of outsourcer in large-scale, long-term outsourcing
arrangement (e.g., through lack of supplier due diligence regarding ﬁnancial
viability, delivery capability and sustainability of supplier’s service)
B. Accepting unreasonable terms of business from IT suppliers
C. Inadequate support and services delivered by vendors, not in line with SLA
D. Noncompliance with software license agreements (use and/or distribution of
unlicensed software)
E. Inability to transfer to alternative suppliers due to overreliance or overdependence
on current supplier
F. Purchase of IT services (especially cloud services) by the business without
consultation /involvement of IT, resulting in inability to integrate the service with in-
house services.
G. Inadequate or unenforced SLA to obtain agreed services and penalties in case of
noncompliance
13 Noncompliance A. Noncompliance with national or international regulations (e.g., privacy, accounting,
manufacturing, environmental, etc.)
B. Lack of awareness of potential regulatory changes that may have a business
impact
C. Operational obstacles caused by regulations
D. Failure to comply with internal procedures
14 Geopolitical issues A. Lack of access due to disruptive incident in other premises
B. Government interference and national policies impacting the business
C. Targeted action from government-sponsored groups or agencies
15 Industrial action A. Facilities and building inaccessible because of labor union strike
B. Third-party providers unable to provide services because of strike
C. Key staff unavailable through industrial action (e.g., transportation or utilities strike)
16 Acts of nature A. Earthquake destroying or damaging important IT infrastructure
B. Tsunami destroying critical premises
C. Major storms and tropical cyclone or tornado damaging critical infrastructure
D. Major wildﬁre

## E. Flooding

F. Rising water table leaving critical location unusable
G. Rising temperature rendering critical locations uneconomical to operate
17 Technology-based
innovation
A. Failure to identify new and important technology trends
B. Failure to appreciate the value and potential of new technologies
C. Failure to adopt and exploit new technologies in a timely manner (functionality,
process optimization, etc.)
D. Failure to provide technology support new business models
18 Environmental A. Environmentally unfriendly equipment (e.g., power consumption, packaging)
19 Data and information
management
A. Discovery of sensitive information by unauthorized persons due to ineﬃcient
retaining/archiving/disposing of information
B. Intentional illicit or malicious modiﬁcation of data
C. Unauthorized disclosure of sensitive information through email or social media
D. Loss of IP and/or leakage of competitive information

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

26
4.  I& T-related issues — A  related m ethod for an I&T  risk assessm ent for the enterprise is to consider w hich I& T-
related issues it currently faces, or, in other w ords, w hat I&T -related risk has m aterialized. T he m ost com m on of
such issues 7
7 include ( figure 2.8 ):

5. T hreat landscape — T he threat landscape under w hich the enterprise operates can be classified as show n in
figure 2.9.

7
7 See also Section 3 .3 .1 T ypical Pain Points, in ISA C A , C O BIT ® 2019 Im plem entation G uide: Im plem enting and O ptim izing an Inform ation and
Technology G overnance Solution , U SA , 2 018.
8
8 T his issue is related to end-user com puting, w hich often stem s from  dissatisfaction w ith IT  solutions and services.

## Figure 2.8— I&T- R elated Issues Design Factor

## Reference Description

A Frustration between different IT entities across the organization because of a perception of low contribution to
business value
B Frustration between business departments (i.e., the IT customer) and the IT department because of failed
initiatives or a perception of low contribution to business value
C Signiﬁcant IT related incidents, such as data loss, security breaches, project failure, application errors, etc.
linked to IT
D Service delivery problems by the IT outsourcer(s)
E Failures to meet IT related regulatory or contractual requirements
F Regular audit ﬁndings or other assessment reports about poor IT performance or reported IT quality or service
problems
G Substantial hidden and rogue IT spending, that is, IT spending by user departments outside the control of the
normal IT investment decision mechanisms and approved budgets
H Duplications or overlaps between various initiatives or other forms of wasting resources
I Insuﬃcient IT resources, staff with inadequate skills or staff burnout/dissatisfaction
J IT-enabled changes or projects frequently failing to meet business needs and delivered late or over budget
K Reluctance by board members, executives or senior management to engage with IT, or lack of committed
business sponsors for IT
L Complex IT operating model and/or unclear decision mechanisms for IT-related decisions
M Excessively high cost of IT
N Obstructed or failed implementations of new initiatives or innovations caused by the current IT architecture
and system
O Gap between business and technical knowledge which leads to business users and IT and/or technology
specialists speaking different languages
P Regular issues with data quality and integration of data across various sources
Q High level of end-user computing, creating (among other problems) a lack of oversight and quality control over
the applications that are being developed and put in operation
R Business departments implementing their own information solutions with little or no involvement of the
enterprise IT department 8
8
S Ignorance and/or noncompliance with security and privacy regulations
T Inability to exploit new technologies or to innovate using I&T

## Figure 2.9 — Threat Landscape Design Factor

## Threat Landscape Explanation

N orm al The enterprise is operating under what are considered normal threat levels
High Due to its geopolitical situation, industry sector or particular proﬁle, the enterprise is
operating in a high-threat environment.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

27

# C H A P TE R  2

B A SIC  C O N C E P TS: G O V E R N A N C E  SYSTE M  A N D C O M P O N E N TS
6. C om pliance requirem ents — the com pliance requirem ents to w hich the enterprise is subject to can be classified
according to the categories listed in figure 2.10.

## 7. R ole of IT — T he role of IT  for the enterprise can be classified as indicated in figure 2.11.

8. Sourcing m odel for IT — T he sourcing m odel the enterprise adopts can be classified as show n in figure 2.12.

9 . IT im plem entation m ethods — T he m ethods the enterprise adopts can be classified as noted in figure 2.13.

9
9 T he roles included in this table are taken from  M cF arlan, F. W arren; Jam es L. M cK enney; Philip Pyburn; “T he Inform ation A rchipelago— Plotting a
C ourse,” H arvard Business Review , January 19 9 3 , https://hbr.org/1983 /01/the-inform ation-archipelago-plotting-a-course .
Figure 2.10— C om pliance R equirem ents Design Factor

## Regulatory Environm ent Explanation

Low  com pliance requirem ents The enterprise is subject to a minimal set of regular compliance requirements that
are lower than average.
N orm al com pliance requirem ents The enterprise is subject to a set of regular compliance requirements that are
common across different industries.
High com pliance requirem ents The enterprise is subject to higher than average compliance requirements, most
often related to industry sector or geopolitical conditions.

## Figure 2.11— R ole of IT Design Factor

## Role of IT 9

9 Explanation
Support IT is not crucial for the running and continuity of the business process and services, nor for
their innovation.
Factory When IT fails, there is an immediate impact on the running and continuity of the business processes
and services. However, IT is not seen as a driver for innovating business processes and services.
Turnaround IT is seen as a driver for innovating business processes and services. At this moment, however, there
is not a critical dependency of IT for the current running and continuity of the business processes
and services.
Strategic IT is critical for both running and innovating the organization’s business processes and services.

## Figure 2.12— Sourcing M odel for IT Design Factor

## Sourcing M odel Explanation

O utsourcing The enterprise calls upon the services of a third party to provide IT services.
C loud The enterprise maximizes the use of the cloud for providing IT services to its users.
Insourced The enterprise provides for their own IT staff and services.
Hybrid A mixed model is applied, combining the three models above in varying degrees.
Figure 2.13 — IT Im plem entation M ethods Design Factor
IT Im plem entation M ethod Explanation
A gile The enterprise uses Agile development working methods for its software development.
DevO ps The enterprise uses DevOps working methods for software building, deployment and operations.
Traditional The enterprise uses a more classic approach towards software development (waterfall) and
separates software development and operations.
Hybrid The enterprise uses a mix of traditional and modern IT implementation, often referred to as
“bimodal IT.”

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

28
10. Technology adoption strategy — T he technology adoption strategy can be classified as listed in figure 2.14.

11. E nterprise size — T w o categories, as show n in figure 2.15 , are identified for the design of an enterprise’s
governance system . 10
10

T he im pact that design factors have on the design of the governance system  is explained in C hapter 3 .
2.6 .1  W hy is There no Industry Sector Design Factor?
E very industry sector has its ow n unique set of requirem ents regarding expectations from  the use of I&T . H ow ever, it
is possible to capture the key characteristics of an industry sector by a com bination of the design factors listed in the
preceding tables. F or exam ple:
T he financial sector can be characterized as follow s: IT  is highly regulated, IT  plays a strategic role, it is typically 
com posed of large enterprises and it operates in a high-threat landscape.
H ealthcare providers (e.g., hospitals) typically aim  for a com bination of client service/stability and innovation 
strategy, are highly regulated, are subject to a num ber of specific risk areas (safety, security, privacy, continuity,
etc.), operate in a m oderate (but increasing) threat landscape, and depend m ore and m ore strategically on IT .
N onprofit enterprises are typically sm aller, and less regulated, have a cost focus, and are not leading innovators in 
technology adoption.
Public sector agencies are often large organizations, w ith client-service and cost-leadership strategies. T hey have 
m oderate to high risk profiles and are highly regulated by their very nature. T he role of IT  can vary, from  support
in conservative agencies, to strategic w hen it com es to egovernm ent initiatives. Sourcing m odels increasingly use
outsourced services, w hereas they are com m only m ainstream  follow ers in technology adoption.
10
10 M icro-enterprises, i.e., enterprises w ith few er than 50 staff m em bers, are not considered in this publication.

## Figure 2.14— Technology A doption Strategy Design Factor

## Technology A doption Strategy Explanation

First m over The enterprise generally adopts new technologies as early as possible and tries to
gain ﬁrst-mover advantage.
Follow er The enterprise typically waits for new technology to become mainstream and proven
before adopting them.
Slow  adopter The enterprise is very late with their adoption of new technologies.

## Figure 2.15— Enterprise Size Design Factor

## Enterprise Size Explanation

Large enterprise (default) Enterprises with more than 250 full-time employees (FTEs)
Sm all and m edium  enterprise Enterprise with 50 to 250 FTEs

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

29

# C H A P TE R  3

# IM PA C T O F DE SIG N  F A C TO R S

C hapter 3

## Im pact of Design Factors

3.1  Im pact of Design Factors
D esign factors influence in different w ays the tailoring of the governance system  of an enterprise. T his publication
distinguishes three different types of im pact, illustrated in figure 3.1 .

M anagem ent objective priority/selection — T he C OB IT  core m odel contains 40 governance and m anagem ent 1.
objectives, each consisting of the process and a num ber of related com ponents. T hey are intrinsically equivalent;
there is no natural order of priority am ong them . H ow ever, design factors can influence this equivalence and
m ake som e governance and m anagem ent objectives m ore im portant than others, som etim es to the extent that
som e governance and m anagem ent objectives m ay becom e negligible. In practice, this higher im portance
translates into setting higher target capability levels for im portant governance and m anagem ent objectives.
E xam ple: W hen an enterprise identifies the m ost relevant enterprise goal(s) from  the enterprise goal list and
applies the goals cascade, this w ill lead to a selection of priority m anagem ent objectives. F or exam ple, w hen
E G 01 Portfolio of com petitive products and services is ranked as very high by an enterprise, this w ill m ake
m anagem ent objective A PO05 M anaged portfolio an im portant part of this enterprise’s governance system .
Figure 3 .1— Im pact of Design Factors on G overnance System

## 1. Management

Objectiv e

## Priority and

Target
Capability
Levels

## 3. Specific

## Focus Areas

## 2. Component

Variations
Design
Factors’
Impa ct

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

30
E xam ple: A n enterprise that is very risk averse w ill give m ore priority to m anagem ent objectives that aspire to
govern and m anage risk and security. G overnance and m anagem ent objectives E D M 03 Ensured risk optim ization ,
A PO12  M anaged risk, A PO13 M anaged security and D SS05 M anaged security services w ill becom e im portant
parts of that enterprise’s governance system  and w ill have higher target capability levels defined for them .
E xam ple: A n enterprise operating w ithin a high threat landscape w ill require highly capable security-related
processes: A PO13 M anaged security and D SS05 M anaged security services.
E xam ple: A n enterprise in w hich the role of IT  is strategic and crucial to the success of the business w ill require
high involvem ent of IT -related roles in organizational structures, a thorough understanding of business by IT
professionals (and vice versa), and a focus on strategic processes such as A PO02 M anaged strategy and A PO08
M anaged relationships .
C om ponents variation : C om ponents are required to achieve governance and m anagem ent objectives. D esign 2.
factors can m andate specific variations of com ponents or can influence the im portance of com ponents.
E xam ple: Sm all and m edium  enterprises m ight not need the full set of roles and organizational structures as laid
out in the C OB IT  core m odel, but m ay use a reduced set instead. T his reduced set of governance and m anagem ent
objectives and the included com ponents is defined in the sm all and m edium  enterprise focus area. 11
1
E xam ple: A n enterprise w hich operates in a highly regulated environm ent w ill attribute m ore im portance to
docum ented w ork products and policies and procedures and to som e roles, e.g., the com pliance officer function.
E xam ple: A n enterprise that uses D evOps in solution developm ent and operations w ill require specific activities,
organizational structures, culture, etc., focused on B A I03 M anaged solutions identification and build and D SS01
M anaged operations .
N eed for specific focus area guidance : som e design factors, such as threat landscape, specific risk, target 3.
developm ent m ethods, infrastructure set-up, w ill drive the need for variation of the core C OB IT  m odel content
to a specific context.
E xam ple: E nterprises adopting a D evOps approach w ill require a governance system  that has a variant of several
generic C OB IT  processes, described in the D evOps focus area guidance 12
2 for C OB IT .
E xam ple: Sm all and m edium  enterprises have less staff, few er IT  resources, and shorter and m ore direct reporting
lines, and differ in m any m ore aspects from  large enterprises. F or that reason, their governance system  for I&T
w ill have to be less onerous, com pared to large enterprises. T his is described in the SM E  focus area guidance of

# C OB IT . 13

3
1
11 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution, the sm all and m edium
enterprise focus area content w as in developm ent and not yet released.
2
12 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution, the D evOps focus
area content w as in developm ent and not yet released.
3
13 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution, the sm all and m edium
enterprise focus area content w as in developm ent and not yet released.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

31

# C H A P TE R  4

DE SIG N IN G  A  T A ILO R E D G O V E R N A N C E  SYSTE M
C hapter 4

## Designing a Tailored G overnance S ystem

4.1  Introduction
Figure 4.1 illustrates the proposed flow  for designing a tailored governance system . E ach step is further discussed in
the subsections that follow .

T he different stages and steps in the design process, as illustrated in figure 4.1 , w ill result in recom m endations for
prioritizing governance and m anagem ent objectives or related governance system  com ponents, for target capability
levels, or for adopting specific variants of a governance system  com ponent.
Som e of these steps or substeps m ay result in conflicting guidance, w hich is inevitable w hen considering a larger
num ber of design factors, the overall generic nature of the design factor guidance and the m apping tables used.
It is recom m ended to put all guidance obtained during the different steps on a design canvas and— in the last stage of
the design process— resolve (to the degree possible) the conflicts am ong the elem ents on the design canvas and
conclude. T here is no m agic form ula. T he final design w ill be a case-by-case decision, based on all the elem ents on
the design canvas. B y follow ing these steps, enterprises w ill realize a governance system  that is tailored to their
needs.
Figure 4.1— G overnance System  Design W orkflow

## 1. Understand

the enterprise
context and
str ategy .

## 2. Determine

the initial
scope of the
governance
system.

## 3. Refine the

scope of the
governance
system.

## 4. Conclude the

governance
system design.
• 1.1 Understand enterprise
s t r a t e g y .
• 1.2 Understand enterprise
g o a l s .
• 1.3 Understand the risk
p r o f i l e .
• 1.4 Understand curr ent
I & T - r e l a t e d  i s s u e s .
• 2.1 Consider enterprise
s t r a t e g y .
• 2.2 Consider enterprise
goals and apply the
COBIT goals cascade.
• 2.3 Consider the risk pr ofile
of the enterprise.
• 2.4 Consider curr ent
I & T - r e l a t e d  i s s u e s .
• 3.1 Consider the thr eat
l a n d s c a p e .
• 3.2 Consider compliance
r e q u i r e m e n t s .
• 3.3 Consider the r ole of I T.
• 3.4 Consider the sour cing
m o d e l .
• 3.5 Consider I T
i m p l e m e n t a t i o n  m e t h o d s .
• 3.6 Consider the I T adoption
s t r a t e g y .
• 3.7 Consider enterprise siz e.
• 4.1 Resolv e inher ent priority
c o n f l i c t s .
• 4.2 Conclude the
g o v e r n a n c e  s y s t e m
d e s i g n .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 20 19  D ES IG N  G U ID E

32
N ote 1 : B efore em barking on the design w orkflow  for a governance system , it is im portant to articulate the unit of
analysis. For exam ple, is the intent to design a governance system  for a business unit, an enterprise as a w hole, a
netw ork of enterprises, etc.? 14
1
N ote 2 : The w orkflow  presented in this publication contains four steps. The substeps w ithin each step are not
m andatory. For exam ple, an enterprise can decide to design a governance system  to address a particular strategy
choice (only) or to address certain areas of IT risk (only), w ithout having to run through the full detailed sequence
of the w orkflow .
4.2  Step 1: U nderstand the Enterprise C ontext and Strategy
In the first step, the enterprise exam ines its context, strategy and business environm ent to achieve a clear
understanding across four partially overlapping, interdependent, and often com plem entary dom ains. The follow ing
subsections outline the critical substeps in Step 1:
Enterprise strategy 
Enterprise goals and resulting alignm ent goals 
I& T risk profile 
C urrent I& T-related issues 
4.2.1  U nderstand Enterprise Strategy
The enterprise m ust determ ine w hich of the archetype enterprise strategies best fit its ow n enterprise strategy. The
archetype enterprise strategies are defined in Section 2 .6, Item  1 (see figu re 2.5 ).
The m echanism  that translates enterprise strategy into a relative rating of im portance of governance and m anagem ent
objectives w orks best w hen clear choices are m ade for enterprise strategy archetypes.
It is generally best to identify one prim ary archetype and select only one secondary archetype. W hen an enterprise
strategy is defined as a m ix of equally im portant strategy archetypes, the governance and m anagem ent objectives
from  the C O B IT core m odel tend to becom e m ore or less equally im portant, thus m aking prioritization difficult.
4.2.2  U nderstand Enterprise G oals
The enterprise strategy is realized through the achievem ent of (a set of) enterprise goals. C O B IT defines a set of 13
generic enterprise goals; each enterprise can/should prioritize its enterprise goals in alignm ent w ith the chosen
enterprise strategy. The list of enterprise goals is defined in Section 2 .6, Item  2  (see figu re 2.6 ).
To translate enterprise goals into a relative rating of im portance of governance and m anagem ent objectives (see the
goals cascade, Section 4 .3.3), one should m ake clear choices w hen selecting enterprise goals. It is recom m ended to
identify only a few  prim ary enterprise goals and a lim ited num ber of secondary enterprise goals. W hen all enterprise
goals are assigned equally im portant priorities, the governance and m anagem ent objectives from  the C O B IT core
m odel tend to becom e m ore or less equally im portant, thus m aking prioritization difficult.
1
14 U nderstanding this scope is fully in line w ith the system  design thinking of recursion, w hich refers to the fact that “any viable enterprise governance
of IT system  contains, and is contained in, a viable enterprise governance of IT system ”; see H uygh, T.; S. D e H aes; “U sing the V iable System  M odel
to Study IT G overnance D ynam ics: Evidence from  a Single C ase Study,” P roceedings of the 51st H aw aii International C onference on System
Sciences , 2 018.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

33

# C H A P TE R  4

DE SIG N IN G  A  T A ILO R E D G O V E R N A N C E  SYSTE M
4.2 .3  U nderstand the R isk P roﬁle
A nother im portant input to the design of a governance system  is to understand the risk profile of the enterprise— that
is, to understand w hich risk scenarios m ay affect the enterprise, and how  to assess their im pact and likelihood of
m aterializing.
T o achieve this understanding, a high-level risk analysis should be perform ed, including:
Identification of relevant risk scenarios (w hich could be based on the list of risk scenario categories defined in 

## Section 2 .6, Item  3 ; see figure 2.7 )

A ssessm ent of im pact and likelihood of the scenario m aterializing, taking into account the current state of risk 
m itigation controls
Overall rating of the risk based on the preceding inputs 
T o be m ost effective in deciding the appropriate risk profile for governance design purposes, one should m ake a clear
differentiation w hile assessing I&T  risk.
W hen all IT  risk is rated as equally im portant, the governance and m anagem ent objectives from  the C OB IT  core
m odel tend to becom e m ore or less equally im portant, thus m aking prioritization difficult.
4.2 .4  U nderstand C urrent I& T -R elated Issues
C losely related to IT  risk are I&T -related issues— also called pain points— from  w hich the enterprise is suffering.
(T hese could be considered risks that have m aterialized.) IT  issues can be identified or reported through risk
m anagem ent, audit, senior m anagem ent or external stakeholders. A  list of com m on issues is defined in Section 2 .5,
Item  4 (see figure 2.8 ).
C lear differentiation should be m ade in rating I&T  issues, in order to provide the necessary inputs to determ ine
governance design priorities.
W hen all I&T -related issues are rated as equally serious, the governance and m anagem ent objectives from  the
C OB IT  core m odel tend to becom e m ore or less equally im portant, thus m aking prioritization difficult.
4.2 .5  C onclusion
A t the end of Step 1, the enterprise w ill have a clear and consistent view  on the enterprise strategy, the enterprise
goals, IT -related risk and current I&T  issues.  In the next step (Section 4.3 ), this inform ation w ill be translated into
prioritized governance/m anagem ent objectives for an initial scoping of a custom ized governance system  for the
enterprise.
4.3  Step 2 : Determ ine the Initial Scope of the G overnance System
T o determ ine the initial scope of the governance system , Step 2  synthesizes inform ation collected during Step 1.
Values derived for enterprise strategy, enterprise goals, risk profile and I&T -related issues are translated into a set of
prioritized governance com ponents to yield the initial tailored governance system  for the enterprise.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

34
4.3.1  Translating Design Factors into G overnance and M anagem ent P riorities
Step 2  presents a num ber of relevant design factors and associated descriptive values, w hose selection w ill drive
prioritization of governance and m anagem ent objectives. T here are tw o basic options for this assessm ent: a
qualitative approach and a m ore quantitative approach.
T he qualitative approach considers the m ost relevant governance and m anagem ent objectives for the values of each
design factor. A fter the initial design and design refinem ent steps (for the latter, see Section 4.4), a qualitative
decision is m ade on governance and m anagem ent objectives priorities.
T he m ore quantitative approach involves num eric m apping tables created for each design factor. T he m apping
tables quantify the descriptive values associated w ith each design factor, in order to indicate their correlation w ith
governance and m anagem ent objectives.
M apping tables in C OB IT ® 2 019  generally contain values betw een zero (0) and four (4). F our indicates m axim um 
relevance of a governance or m anagem ent objective w ith that particular design factor value;  zero indicates no
relevance.
T ranslating design factor values into governance and m anagem ent objective im portance involves a m atrix 
calculation, resulting in a score for each governance and m anagem ent objective.
D epending on the actual m ethod preferred, these scores can be further m anipulated for presentation purposes (e.g., 
norm alized to certain fixed scales).
A t the end of Steps 2  and 3 , the results of several of these calculations need to be consolidated. A gain, there is no 
objectively necessary, fixed m ethod for consolidation; how ever, it is often best accom plished using a (w eighted)
sum m ation.
C hapter 7 of this publication includes exam ples of the quantitative approach. A ll exam ples reference an E xcel ®
toolkit that is available from  w w w.isaca.org/ C O BIT/Pages/C O BIT-2019-D esign-G uide.aspx as a com panion to this
C O BIT ® 2019 D esign G uide .
4.3.2   C onsider E nterprise Strategy (Design Factor 1)
F or each enterprise strategy archetype, figure 4.2 lists the m ost im portant governance and m anagem ent objectives,
im portant governance com ponents and relevant focus area guidance. W hen enterprise strategy is defined as a hybrid
strategy, the im portant governance and m anagem ent objectives w ill reflect a com bination of elem ents.

2
15 ‘Im portant’ corresponds to a value of 3  or m ore in the m apping table of this design factor to governance and m anagem ent objectives.
Figure 4.2— G overnance and M anagem ent O bjectives P riority M apped to Enterprise Strategy Design
Factor

## Design Factor Value

G overnance and
M anagem ent O bjectives
Priority
C om ponents Focus A rea Variants
Growth/acquisition Important management
objectives 15
2 include:

# APO02, APO03, APO05 

# BAI01, BAI05, BAI11 

Important components:
Organizational structures 
Support the portfolio management 
role with an investment oﬃce
Enterprise architect 
Services, infrastructure and 
applications
Facilitate automation and growth and 
realize economies of scale
COBIT core model

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

35

# C H A P TE R  4

DE SIG N IN G  A  T A ILO R E D G O V E R N A N C E  SYSTE M
4.3.3  C onsider E nterprise G oals and A pply the C O B IT G oals C ascade (Design Factor 2 )
T he enterprise strategy is realized by achieving (a set of) enterprise goals. C OB IT ® 2 019  defines 13  generic
enterprise goals (see Section 2 .6, Item  2  and figure 2.6 ); each enterprise should prioritize these enterprise goals in
alignm ent w ith the enterprise strategy.
T o translate enterprise goals into actionable governance and m anagem ent objectives:
Start w ith the generic enterprise goals, and determ ine the m ost im portant enterprise goals for the organization. 1.
Select the top three to five m ost im portant enterprise goals; too m any high-priority goals w ill produce less
m eaningful goals cascade results.
F ind the prioritized enterprise goals on the m apping table betw een enterprise goals and alignm ent goals 2.
(A ppendix B ). U se the m apping to determ ine the m ost im portant alignm ent goals.
F ind the prioritized alignm ent goals on the m apping table betw een alignm ent goals and governance and 3.
m anagem ent objectives (A ppendix C ). U se the m apping to determ ine the m ost im portant governance and
m anagem ent objectives.
T his substep identifies a num ber of governance and m anagem ent objectives that have higher im portance for the
enterprise, based on the prioritized enterprise goals.
N ote : T his technique is purely m echanical, using m apping tables that are generic in nature. T he enterprise m ust
interpret the results w ith care, or adapt the m apping tables based on its ow n experience and context. In the
w orkflow  described in this guide, this fine-tuning is done in Step 4 C onclude the governance system  design .
Figure 4.2— G overnance and M anagem ent O bjectives P riority M apped to Enterprise Strategy Design
Factor (cont.)

## Design Factor Value

G overnance and
M anagem ent O bjectives
Priority
C om ponents Focus A rea Variants
Innovation/
differentiation
Important management
objectives include:

# APO02, APO04, APO05 

# BAI08, BAI11 

Important components:
Organizational structures 
Chief digital oﬃcer and/or chief 
innovation oﬃcer
Important inﬂuence of culture and 
behavior component for innovation
COBIT core model
Cost leadership Important governance and
management objectives
include:

# EDM04 

# APO06, APO10 

Important components:
Skills and competencies 
Focus on IT costing and budgeting 
skills
Important inﬂuence of culture and 
behavior component
Services, infrastructure and 
applications component (e.g., for
automation of controls, improving
eﬃciency)
COBIT core model
Client service/stability Important governance and
management objectives
include:

# EDM02 

# APO08, APO09, APO11 

# BAI04 

# DSS02, DSS03, DSS04 

Important component:
Important inﬂuence of culture and 
behavior component (client centricity)
COBIT core model

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

36
E xam ples of goals cascade application are included in the toolkit com panion to this C O BIT ® 2019 D esign G uide .16
3
4.3.4  C onsider the R isk P roﬁle of the E nterprise (Design Factor 3)
In Step 1 (see Section 4.2 .3  U nderstand the R isk Profile), the enterprise perform ed a high-level risk analysis to
identify risk categories exceeding the enterprise’s risk appetite. H ere, the results of the risk analysis are translated
into priorities for governance and m anagem ent objectives. T he m ost com m on risk response used in risk m anagem ent
is risk m itigation, w hich requires a num ber of controls (in risk language) to be im plem ented, or (in the language of
C OB IT ), governance and m anagem ent objectives that need to be achieved. A ppendix D  contains a m apping betw een
the 19  IT  risk categories in C OB IT ® 2 019  and the governance and m anagem ent objectives, expressing the extent to
w hich each governance and m anagem ent objective can be considered as a control for each risk scenario.
T he m apping table in A ppendix D  relates the risk profile of the enterprise to governance and m anagem ent objectives
and their priorities, using the sam e technique and scoring m ethod described earlier.
E xam ple : A ppendix D  illustrates that if IT  risk scenario category 1 (R ISK C AT 01) IT investm ent decision m aking,
portfolio definition &  m aintenance is a concern, then the follow ing governance and m anagem ent objectives w ill be
im portant:

# • E D M 01, E D M 02 , E D M 04, E D M 05

# • A PO05

4.3.5  C onsider C urrent I& T -R elated Issues of the E nterprise (Design Factor 4)
In Step 1 (see Section 4.2 .4 U nderstand C urrent I&T -R elated Issues), the enterprise perform ed a high-level
diagnostic on the I&T -related issues it experiences. H ere, the results of this diagnostic are translated into priorities
for governance and m anagem ent objectives.
A ppendix E  contains a m apping table betw een I&T  issues and C OB IT ® 2 019  governance and m anagem ent objectives. A s
A ppendix E  show s, each I&T -related issue is associated to one or m ore governance or m anagem ent objective that can
influence the I&T -related issue. T he sam e techniques and scoring m echanism s described earlier can be used.
E xam ple : W hen the I&T -related issue, “IT -enabled changes or projects frequently failing to m eet business needs
and delivered late or over budget,” is of concern, the follow ing governance and m anagem ent objectives are
im portant:

# • A PO03

# • B A I01, B A I02 , B A I03 , B A I05, B A I11

4.3.6   C onclusion
A t the end of Step 2 , all elem ents are available to define the initial scope of a custom ized governance system :
Prioritized governance and m anagem ent objectives indicate w hich governance and m anagem ent objectives 
should be the focus.
Guidance on specific governance com ponents can potentially also be included in the initial design. 
3
16 T he com panion toolkit can be dow nloaded at w w w.isaca.org/C O BIT/Pages/C O BIT-2019-D esign-G uide.aspx .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

37

# C H A P TE R  4

DE SIG N IN G  A  T A ILO R E D G O V E R N A N C E  SYSTE M
T he enterprise can choose to elaborate the current initial design and resolve all differences am ong the various inputs;
or, the enterprise can w ait until Step 4 of the w orkflow  and com bine the different inputs w ith the scope refinem ents
identified in Step 3 .
4.4  Step 3: R eﬁne the Scope of the G overnance System
Step 3  identifies refinem ents to the initial scope of the governance system , based on the rem aining set of design
factors as defined in Section 2 .6. T hroughout this chapter, not all design factors m ay be applicable to each enterprise.
T hose not applicable can be ignored.
In this step, the governance system  designer w ill:
W alk through each design factor (D F ) from  D F 5 Threat landscape through D F 11 Enterprise size .1.
D eterm ine w hether or not each design factor is applicable. 2.
F or applicable design factors, determ ine w hich of the potential values— or w hich com bination of potential 3.
values— is m ost applicable to the enterprise. R eference descriptions of the applicable design factor values, along
w ith the m apping tables in A ppendices F  through K , to determ ine w hich refinem ents to the governance system
are associated w ith these values.
T he result of each consideration of a design factor is a ranked list of governance and m anagem ent objectives, sim ilar
to the result from  Step 2 . U sing the m apping tables in A ppendices F  through K , the sam e techniques and scales can
be used as described earlier.
4.4.1  C onsider the Threat Landscape (Design Factor 5)
T he follow ing steps should be perform ed w hen considering this design factor:
D ecide w hich com bination of values best fits the current situation of the enterprise, as per the defined entries in 
figure 4.3 .
C onsider the listed guidance for governance and m anagem ent objectives, com ponents and focus areas, and include 
the pertinent inform ation on the design canvas for resolution and conclusion in Step 4.

4
17 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the inform ation
security focus area content w as in developm ent, and not yet released.
Figure 4.3 — G overnance and M anagem ent O bjectives P riority M apped to Threat Landscape Design
Factor
Design
Factor
Value
G overnance and M anagem ent
O bjectives Priority C om ponents Focus A rea Variants

## High Important governance and

management objectives include:

# EDM01, EDM03 

# APO01, APO03, APO10, APO12,

# APO13, APO14

# BAI06, BAI10 

# DSS02, DSS04, DSS05, DSS06 

# MEA01, MEA03, MEA04 

Important organizational structures include:
Security strategy committee 
Chief information security oﬃcer (CISO) 
Important culture and behavior aspects include:
Security awareness 
Information ﬂows include:
Security policy 
Security strategy 
Information security
focus area 17
4
Normal  As per the initial scope deﬁnition   N /A  COBIT core model

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

38
4.4.2   C onsider C om pliance R equirem ents (Design Factor 6 )
T he follow ing steps should be perform ed w hen considering this design factor:
D ecide w hich com bination of values best fits the current situation of the enterprise, as per the defined entries in 
figure 4.4 .
C onsider the listed guidance for governance and m anagem ent objectives, com ponents and focus areas, and include 
the pertinent inform ation on the design canvas for resolution and conclusion in Step 4.

4.4.3  C onsider the R ole of IT (Design Factor 7)
T he follow ing steps should be perform ed w hen considering this design factor:
D ecide w hich com bination of values best fits the current situation of the enterprise, as per the defined entries in 
figure 4.5 .
C onsider the listed guidance for governance and m anagem ent objectives, com ponents and focus areas, and include 
the pertinent inform ation on the design canvas for resolution and conclusion in Step 4.

5
18 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the inform ation
security focus area content w as in developm ent and not yet released.
6
19 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the D evOps focus
area content w as in developm ent and not yet released.
Figure 4.4— G overnance and M anagem ent O bjectives P riority M apped to C om pliance R equirem ents

## Design Factor

Design
Factor
Value
G overnance and M anagem ent
O bjectives Priority C om ponents Focus A rea Variants

## High Important governance and

management objectives include:

# EDM01, EDM03 

# APO12 

# MEA03, MEA04 

Importance of compliance function:
High relevance of documentation 
(information items) and policies and
procedures
COBIT core model
Normal  As per the initial scope deﬁnition   N /A  COBIT core model
Low  As per the initial scope deﬁnition   N /A  COBIT core model
Figure 4.5— G overnance and M anagem ent O bjectives P riority M apped to R ole of IT Design Factor

## Design Factor

Value
G overnance and M anagem ent
O bjectives Priority C om ponents Focus A rea Variants
Support  As per the initial scope deﬁnition   N /A  COBIT core model

## Factory Important governance and

management objectives include:

# EDM03 

# DSS01, DSS02, DSS03, DSS04 

N /A  Information security
focus area 18
5

## Turnaround Important governance and

management objectives include:

# APO02, APO04 

# BAI02, BAI03 

N /A  DevOps focus area 19
6

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

39

# C H A P TE R  4

DE SIG N IN G  A  T A ILO R E D G O V E R N A N C E  SYSTE M
4.4.4  C onsider the Sourcing M odel for IT (Design Factor 8)
T he follow ing steps should be perform ed w hen considering this design factor:
D ecide w hich com bination of values best fits the current situation of the enterprise, as per the defined entries in 
figure 4.6 .
C onsider the listed guidance for governance and m anagem ent objectives, com ponents and focus areas, and include 
the pertinent inform ation on the design canvas for resolution and conclusion in Step 4.

4.4.5  C onsider IT Im plem entation M ethods (Design Factor 9)
T he follow ing steps should be perform ed w hen considering this design factor:
D ecide w hich com bination of values best fits the current situation of the enterprise, as per the defined entries in 
figure 4.7 .
7
2 0 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the digital
transform ation focus area content w as being contem plated as a potential future focus area.
8
2 1 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the vendor
m anagem ent focus area w as being contem plated as a potential future focus area.
9
2 2 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the cloud focus area
w as being contem plated as a potential future focus area.
Figure 4.5— G overnance and M anagem ent O bjectives Priority M apped to Role of IT Design Factor (cont.)

## Design Factor

Value
G overnance and M anagem ent
O bjectives Priority C om ponents Focus A rea Variants

## Strategic Important governance and

management objectives include:

# EDM01, EDM02, EDM03 

# APO02, APO04, APO05, APO12,

# APO13

# BAI02, BAI03 

# DSS01, DSS02, DSS03, DSS04,

# DSS05

Typical bimodal components include:
Organizational structures 
Chief digital oﬃcer 
Skills and competencies 
Staff who can work in an ambidextrous 
environment that combines both
exploration and exploitation
Processes 
A portfolio and innovation process that 
integrates exploration and exploitation
of digital transformation opportunities
Digital transformation
focus area 20
7
Figure 4.6 — G overnance and M anagem ent O bjectives Priority M apped to Sourcing M odel for IT Design Factor
Design

## Factor Value

G overnance and M anagem ent O bjectives
Priority C om ponents Focus A rea Variants
Outsourcing Important management objectives include:

# APO09, APO10 

# MEA01 

N /A  Vendor management
focus area 21
8
Cloud Important management objectives include:

# APO09, APO10 

# MEA01 

N /A  Cloud focus area 22
9
Insourced  As per the initial scope deﬁnition   N /A  COBIT core model
Hybrid Com bination of guidance for the three speciﬁc options

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

40
C onsider the listed guidance for governance and m anagem ent objectives, com ponents and focus areas, and include 
the pertinent inform ation on the design canvas for resolution and conclusion in Step 4.

4.4.6   C onsider the T echnology A doption Strategy (Design Factor 10 )
T he follow ing steps should be perform ed w hen considering this design factor:
D ecide w hich com bination of values best fits the current situation of the enterprise, as per the defined entries in 
figure 4.8 .
C onsider the listed guidance for governance and m anagem ent objectives, com ponents and focus areas, and include 
the pertinent inform ation on the design canvas for resolution and conclusion in Step 4.

10
2 3 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the A gile focus area
w as being contem plated as a potential future focus area.
11
2 4 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the D evOps focus
area content w as in developm ent and not yet released.
12
2 5 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the digital
transform ation focus area content w as being contem plated as a potential future focus area.
Figure 4.7 — G overnance and M anagem ent O bjectives P riority M apped to IT Im plem entation M ethods

## Design Factor

Design
Factor
Value
G overnance and M anagem ent
O bjectives Priority C om ponents Focus A rea Variants
Agile Important management objectives
include:

# BAI02, BAI03, BAI06 

Important and speciﬁc roles as identiﬁed in 
the Agile focus area guidance
Agile focus area 23
10
DevOps Important management objectives
include:

# BAI03 

Important and speciﬁc roles as identiﬁed in 
the DevOps focus area guidance
DevOps focus area 24
11
Traditional  As per the initial scope deﬁnition   N /A  COBIT core model
Hybrid Com bination of guidance for the three speciﬁc options
Figure 4.8— G overnance and M anagem ent O bjectives P riority M apped to Technology A doption

## Strategy Design Factor

Design Factor Value G overnance and M anagem ent O bjectives
Priority
C om ponents Focus A rea Variants
First Mover Important governance and management
objectives include:

# EDM01, EDM02 

# APO02, APO04, APO05, APO08 

# BAI01, BAI02, BAI03, BAI05, BAI07, BAI11 

# MEA01 

N /A  DevOps focus area 24
Digital transformation
focus area 25
12
Follower Important governance and management
objectives include:

# APO02, APO04 

# BAI01 

N /A  COBIT core model
Slow Adopter  As per the initial scope deﬁnition   N /A  COBIT core model

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

41

# C H A P TE R  4

DE SIG N IN G  A  T A ILO R E D G O V E R N A N C E  SYSTE M
4.4.7  C onsider E nterprise Size (Design Factor 11)
T he follow ing steps should be perform ed w hen considering this design factor:
D ecide w hich com bination of values best fits the current situation of the enterprise, as per the defined entries in 
figure 4.9 .
C onsider the listed guidance for governance and m anagem ent objectives, com ponents and focus areas, and include 
the pertinent inform ation on the design canvas for resolution and conclusion in Step 4.

E xam ple : If the enterprise is an SM E  (e.g., it has 2 50 or few er full-tim e em ployees [F T E s]), it should use the
guidance contained in the SM E  focus area for the design of its governance system .
4.4.8  C onclusion
A t  the end of Step 3 , the enterprise w ill have identified a series of potential refinem ents for the initial governance
system  and put them  all on the canvas for consolidation during Step 4 of the design w orkflow .
T he follow ing refinem ents are typically expressed sim ilar to outcom e from  Step 2 : prioritized governance and
m anagem ent objectives, im portant com ponents for the governance system , and specific focus area guidance.
4.5  Step 4: R esolve C onﬂicts and C onclude the G overnance System  Design
A s the last step in the design process, Step 4 brings together all inputs from  previous steps to conclude the
governance system  design, as depicted in figure 4.10 . T he resulting governance system  m ust reflect careful
consideration of all inputs— understanding that these inputs m ay som etim es conflict.
13
2 6 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution, the sm all and m edium
enterprise focus area content w as in developm ent and not yet released.
Figure 4.9 — G overnance and M anagem ent O bjectives P riority M apped to Enterprise Size Design
Factor

## Design Factor Value

G overnance and
M anagem ent O bjectives
Priority
C om ponents Focus A rea Variants
Large  As per the initial scope 
deﬁnition
N /A  COBIT core model
Small/Medium  As per the initial scope 
deﬁnition
As applicable in the SM E focus area 
description
SME focus area 26
13

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

42

4.5.1  R esolve Inherent P riority C onﬂicts
Step 4 involves reconciling any conflicts in order to finalize the design.
4.5.1.1  P urpose
T he follow ing outputs from  previous steps w ill be considered before any conclusion is m ade:
Initial design of the governance system , as obtained during Step 2 , based on the enterprise strategy, enterprise 
goals, risk profile and I&T -related issues. T his initial design probably reflects som e diverging sets of prioritized
m anagem ent objectives.
Scope refinem ents obtained in Step 3  through the analysis of rem aining design factors and diverging sets of priorities. 
4.5.1.2   R esolution Strategies
T he w orkflow  described in this guide can be applied to different situations, requiring different strategies for com ing
to a conclusion. In short, the enterprise needs to analyze the data and results after applying design factors in the
context of its goals for im plem enting a governance program .
E xam ple : If the enterprise has one im portant, ongoing initiative (e.g., a m ajor investm ent in an enterprise
application, digital transform ation program , etc.) or w ants to focus on a very specific topic or issue (e.g., solving
an im portant security problem , adopting a D evOps approach, aligning to and com plying w ith new  privacy
regulations, etc.), the enterprise need not apply all steps in the proposed w orkflow  in full detail, but rather, m ay
focus on specific areas of interest.
• In case of an im portant developm ent investm ent, the enterprise can consider its enterprise strategy (design factor
1) as an innovation/differentiation strategy, and consequently decide to w ork only on the governance and
m anagem ent objectives that are em phasized for this design factor.
•   In case of new  privacy regulations, an enterprise can focus on governance and m anagem ent objectives that
correspond to high com pliance requirem ents (design factor 6). T hose objectives are E D M 01 Ensured
governance fram ew ork setting and m aintenance , E D M 03  Ensured risk optim ization , A PO12  M anaged risk ,
M E A 03  M anaged com pliance w ith external requirem ents and M E A 04 M anaged assurance . In addition, the
enterprise w ill need to focus on governance and m anagem ent objectives that com e out of the com pliance
requirem ents analysis contained in M E A 03 .
Figure 4.10— G overnance System  Design Step 4— C onclusion

## Understand the

enterprise context
and str ategy

## Determine the

initial scope of the
governance system

## Refine the

scope of the
governance system
Scope r efinement Initial scope
Resolv e
conflicts and
conclude the
governance system
design

## Tailored Governance System

## Governance System Canvas

EDM01 —Ensur ed
Governance

## Framework Setting

## and  Maintenance

APO01—Managed

## IT Management

Framework
APO08—Managed
Relationships
APO02—Managed
Strategy
APO09—Managed
Service
Agr eements
APO03—Managed
Enterprise
Architecture
APO10—Managed
Vendors
APO04—Managed
Inno vation
APO11—Managed
Quality
APO05—Managed
Portfolio
APO12—Managed
Risk
APO06—Managed

## Budget and Costs

APO07—Managed
Human Resour ces
APO014—Managed
Data
MEA01 —Managed

## Performance and

Conformance
Monitoring
MEA02 —Managed

## System of Internal

Contr ol

## MEA03— Managed

## Compliance With

External
Requir ements

## MEA04— Managed

Assur ance
APO13—Managed
Security
DSS01—Managed
Oper ations
DSS02—Managed

## Service Requests

and  Incid ents
DSS03—Managed
Problems
DSS04—Managed
Continuity
DSS05—Managed
Security
Services
DSS06—Managed
Business

## Process Controls

BAI01 —Managed
Programs
BAI08 —Managed
Knowledge
BAI02 —Managed
Requir ements
Definition
BAI09 —Managed
Assets
BAI03 —Manage
Solutions
Identification

## and  Build

BAI10 —Managed
Configur ation
BAI04 —Managed
Availability

## and Capacity

BAI11 —Managed
Projects
BAI05 —Managed
Organizational
Change
BAI06 —Managed

## IT Changes

BAI07 —Managed

## IT Change

## Acceptance and

Transitioning
EDM02 —Ensur ed

## Benefits Delivery

EDM03 —Ensur ed

## Risk  Optimization

EDM04 —Ensur ed
Resour ce
Optimization
EDM05 —Ensur ed
Stakeholder
Engagement
EDM01—En sured
Governance

## Framework Setting

## and Maintenance

APO0 1—Man aged

## IT Management

Framework
APO0 8—Man aged
Relationships
APO0 2—Manage d
Str ate gy
APO0 9—Manage d
Service
Agr eements
APO0 3—Manage d
Enterprise
Architecture
APO1 0—Manage d
Vendors
APO0 4—Manage d
Innovation
APO1 1—Manage d
Quality
APO0 5—Manage d
Portfolio
APO1 2—Man aged
Risk
APO0 6—Manage d

## Budget and Costs

APO0 7—Manage d

## Human Resources

APO0 14—Manage d
Data
MEA01—Manage d

## Performance and

Conforman ce
Mon itoring
MEA02—Manage d

## System of In ternal

Con trol
MEA03— Man aged
Complian ce With
External
Requirements
MEA04— Man aged
Assu rance
APO1 3—Manage d
Security
DSS01—Manage d
Ope rations
DSS02—Manage d

## Service Requests

## and Incidents

DSS03—Manage d
Problems
DSS04—Manage d
Contin uity
DSS05—Manage d
Security
Services
DSS06—Manage d
Business

## Process Controls

BAI01 —Manage d
Programs
BAI0 8—Manage d
Knowledge
BAI02 —Man age d
Requirements
Definition
BAI0 9—Manage d
Asse ts
BAI03 —Man age
Solu tion s
Ide ntification

## and Build

BAI1 0—Manage d
Configu ration
BAI04 —Manage d
Availability

## and Capacity

BAI11 —Manage d
Projects
BAI05 —Manage d
Organizational
Chan ge
BAI0 6—Manage d

## IT Changes

BAI0 7—Manage d

## IT Change

## Acceptance and

Transitioning
EDM02—En sured

## Benefits Delivery

EDM03—En sured

## Risk Optimization

EDM04—En sured
Resource
Optimiz ation
EDM05—En sured
Stak eholder
Engagement
EDM01 —Ensur ed
Governance

## Framework Setting

## and  Maintenance

APO01—Managed

## IT Management

Framework
APO08—Managed
Relationships
APO02—Managed
Strategy
APO09—Managed
Service
Agr eements
APO03—Managed
Enterprise
Architecture
APO10—Managed
Vendors
APO04—Managed
Inno vation
APO11—Managed
Quality
APO05—Managed
Portfolio
APO12—Managed
Risk
APO06—Managed

## Budget and Costs

APO07—Managed
Human Resour ces
APO014—Managed
Data
MEA01 —Managed

## Performance and

Conformance
Monitoring
MEA02 —Managed

## System of Internal

Contr ol

## MEA03— Managed

## Compliance With

External
Requir ements

## MEA04— Managed

Assur ance
APO13—Managed
Security
DSS01—Managed
Oper ations
DSS02—Managed

## Service Requests

and Incid ents
DSS03—Managed
Problems
DSS04—Managed
Continuity
DSS05—Managed
Security
Services
DSS06—Managed
Business

## Process Controls

BAI01 —Managed
Programs
BAI08 —Managed
Knowledge
BAI02 —Managed
Requir ements
Definition
BAI09 —Managed
Assets
BAI03 —Manage
Solutions
Identification

## and  Build

BAI10 —Managed
Configur ation
BAI04 —Managed
Availability

## and Capacity

BAI11 —Managed
Projects
BAI05 —Managed
Organizational
Change
BAI06 —Managed

## IT Changes

BAI07 —Managed

## IT Change

## Acceptance and

Transitioning
EDM02 —Ensur ed

## Benefits Delivery

EDM03 —Ensur ed

## Risk  Optimization

EDM04 —Ensur ed
Resour ce
Optimization
EDM05 —Ensur ed
Stakeholder
Engagement
EDM01 —Ensur ed
Governance

## Framework Setting

## and  Maintenance

APO01—Managed

## IT Management

Framework
APO08—Managed
Relationships
APO02—Managed
Strategy
APO09—Managed
Service
Agr eements
APO03—Managed
Enterprise
Architecture
APO10—Managed
Vendors
APO04—Managed
Inno vation
APO11—Managed
Quality
APO05—Managed
Portfolio
APO12—Managed
Risk
APO06—Managed

## Budget and Costs

APO07—Managed
Human Resour ces
APO014—Managed
Data
MEA01 —Managed

## Performance and

Conformance
Monitoring
MEA02 —Managed

## System of Internal

Contr ol

## MEA03— Managed

## Compliance With

External
Requir ements

## MEA04— Managed

Assur ance
APO13—Managed
Security
DSS01—Managed
Oper ations
DSS02—Managed

## Service Requests

and Incid ents
DSS03—Managed
Problems
DSS04—Managed
Continuity
DSS05—Managed
Security
Services
DSS06—Managed
Business

## Process Controls

BAI01 —Managed
Programs
BAI08 —Managed
Knowledge
BAI02 —Managed
Requir ements
Definition
BAI09 —Managed
Assets
BAI03 —Manage
Solutions
Identification

## and  Build

BAI10 —Managed
Configur ation
BAI04 —Managed
Availability

## and Capacity

BAI11 —Managed
Projects
BAI05 —Managed
Organizational
Change
BAI06 —Managed

## IT Changes

BAI07 —Managed

## IT Change

## Acceptance and

Transitioning
EDM02 —Ensur ed

## Benefits Delivery

EDM03 —Ensur ed

## Risk  Optimization

EDM04 —Ensur ed
Resour ce
Optimization
EDM05 —Ensur ed
Stakeholder
Engagement
EDM01 —Ensur ed
Governance

## Framework Setting

## and  Maintenance

APO01—Managed

## IT Management

Framework
APO08—Managed
Relationships
APO02—Managed
Strategy
APO09—Managed
Service
Agr eements
APO03—Managed
Enterprise
Architecture
APO10—Managed
Vendors
APO04—Managed
Inno vation
APO11—Managed
Quality
APO05—Managed
Portfolio
APO12—Managed
Risk
APO06—Managed

## Budget and Costs

APO07—Managed
Human Resour ces
APO014—Managed
Data
MEA01 —Managed

## Performance and

Conformance
Monitoring
MEA02 —Managed

## System of Internal

Contr ol

## MEA03— Managed

## Compliance With

External
Requir ements

## MEA04— Managed

Assur ance
APO13—Managed
Security
DSS01—Managed
Oper ations
DSS02—Managed

## Service Requests

and  Incid ents
DSS03—Managed
Problems
DSS04—Managed
Continuity
DSS05—Managed
Security
Services
DSS06—Managed
Business

## Process Controls

BAI01 —Managed
Programs
BAI08 —Managed
Knowledge
BAI02 —Managed
Requir ements
Definition
BAI09 —Managed
Assets
BAI03 —Manage
Solutions
Identification

## and  Build

BAI10 —Managed
Configur ation
BAI04 —Managed
Availability

## and  Capacity

BAI11 —Managed
Projects
BAI05 —Managed
Organizational
Change
BAI06 —Managed

## IT Changes

BAI07 —Managed

## IT Change

## Acceptance and

Transitioning
EDM02 —Ensur ed

## Benefits Delivery

EDM03 —Ensur ed

## Risk  Optimization

EDM04 —Ensur ed
Resour ce
Optimization
EDM05 —Ensur ed
Stakeholder
Engagement

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

43

# C H A P TE R  4

DE SIG N IN G  A  T A ILO R E D G O V E R N A N C E  SYSTE M
E xam ple : If the enterprise requires a broad, holistic and com prehensive view of its governance system , it is
recom m ended that the enterprise apply the full w orkflow  as described in this guide and carefully consider all
design factors.
W hen defining the design of a governance system , the enterprise should review  its governance and m anagem ent
objectives, and analyze its current perform ance level(s) (i.e., capability levels for processes). T he enterprise should
then take the results of these assessm ents into account w hen defining the road m ap tow ard the target governance
system , looking first of all for quick w ins (i.e., those initiatives entailing lim ited effort, but yielding high benefit).
4.5.1.3  R esolution A pproach
T here are no universally applicable guidelines for resolving com peting or conflicting priorities, valid across all
enterprise contexts. H ow ever, a few  recom m endations to approach this are:
Include all key stakeholders in the discussion on the design of the governance system : board and executive 
m anagem ent, business executives, m anagem ent of the IT  function, and risk and assurance m anagem ent.
C onsider the generic nature of C OB IT  guidance and the m apping tables, w hich cannot take into account all 
specificities of every enterprise. T he enterprise can and should be prepared to deviate from  som e of the identified
priorities if it feels there are justified reasons for such deviation.
Likew ise, note that the specific context of the enterprise m ay w ell require deviating from  the kind of strictly 
quantitative priorities for governance and m anagem ent objectives that are generated by generic, preprogram m ed
com putations (e.g., results from  m athem atical m atrix calculations).
4.5.2   C onclude the G overnance System  Design
4.5.2 .1  C oncluding the Design
T he conclusion of the design phase m ust result in one design for the governance system  for enterprise I&T . T his
design w ill include:
Prioritized governance and m anagem ent objectives, w hereby the: 
N um ber of high-priority objectives is kept to a reasonable level. 
T arget capability levels (or equivalent perform ance requirem ents for nonprocesses) are defined, w ith higher 
target capability levels for the m ost critical objectives, and low er target capability levels for less critical
objectives.
A  variety of target capability levels for processes (or equivalent perform ance targets for other com ponents). W hen 
defining those targets, it is not recom m ended to aim  for the highest rating, because:
F or som e processes or other com ponents, a level five (5) capability is not possible or defined. 
Very rarely is it cost-effective or justifiable to operate a governance system  at this high capability level across all 
objectives.
M any organizations w ill find it nearly im possible to im plem ent the road m ap tow ard such a high capability level 
governance system  w ithin any sort of reasonable tim e fram e.
A  governance com ponent requiring specific attention due to a particular issue or circum stance (e.g., if privacy is of 
utm ost concern to an enterprise, privacy policies and procedures m ay need extra attention)
F ocus area guidance com plem enting the core C OB IT  guidance (w hen available, necessary and appropriate) 
E xam ples of such a design are included in C hapter 7.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

44

# C O B IT ® 20 19 D ESIG N  G U ID E

4.5 .2.2  S ustaining the G overnance S ystem
T he result of the last step in the governance design w orkflow  is a w ell-designed governance system . A  governance
system , how ever, is inherently dynam ic. Strategies can change, im portant investm ent program s are launched, threat
landscapes change, technologies change, etc. T his m eans that the governance system  should be review ed on a regular
basis, and changes to the system  should be m ade w henever necessary.
T his dynam ic nature of any governance system  also inform s the C O BIT ® 2019 Im plem entation G uide , w hich
outlines a continuous im provem ent cycle (see also C hapter 5 of this publication).

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

45

# C H A P TE R  5

C O N N E C TIN G  W ITH  TH E  CO BIT ® 2019 IM PLEM EN T A TIO N  G UID E
C hapter 5
Connecting W ith the C O B IT ® 20 19  Im plem entation G uide
5.1  P urpose of the C O B IT ® 2019 Im plem entation G uide
T he C O BIT ® 2019 Im plem entation G uide em phasizes an enterprisew ide view  of governance of I&T , recognizing that
I&T  are pervasive in enterprises, and that it is neither possible, nor good practice, to separate business and IT -related
activities.
T he governance and m anagem ent of enterprise I&T  should, therefore, be im plem ented as an integral part of
enterprise governance, covering the full end-to-end business and IT  functional areas of responsibility.
W hen governance system  im plem entations fail, one of the com m on reasons is that they are not initiated and then
m anaged properly as program s, to ensure that benefits are realized. G overnance program s m ust be sponsored by
executive m anagem ent and properly scoped, and should alw ays define objectives that are attainable. T hese
provisions enable the enterprise to absorb the pace of change as planned. Program  m anagem ent is, therefore,
addressed as an integral part of the im plem entation life cycle.
W hile a program  and project approach is recom m ended to drive im provem ent initiatives effectively, the overarching
goal is to establish a norm al business practice and a sustainable approach to governing and m anaging enterprise I&T
(as w ith any other aspect of enterprise governance). F or this reason, the im plem entation approach is based on
em pow ering business and IT  stakeholders to take ow nership of I&T -related governance and m anagem ent decisions
and activities by facilitating and enabling change.
T he im plem entation program  closes w hen the process for focusing on IT -related priorities and governance
im provem ent generates a m easurable benefit, and the results of the program  have becom e em bedded in ongoing
business activity.
M ore inform ation on these subjects can be found in the C O BIT ® 2019 Im plem entation G uide .
5.2   C O B IT Im plem entation A pproach
T he C OB IT  im plem entation approach is sum m arized in Figure 5.1 .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

46

5.2 .1  P hase 1— W hat A re the Drivers?
Phase 1 of the im plem entation approach identifies current change drivers and creates at executive m anagem ent levels
a desire to change that is then expressed in an outline of a business case. A  change driver is an internal or external
event, condition or key issue that serves as a stim ulus for change. E vents, trends (industry, m arket or technical),
perform ance shortfalls, softw are im plem entations and even the goals of the enterprise can all act as change drivers.
R isk associated w ith im plem entation of the program  itself is described in the business case and m anaged throughout
the life cycle. Preparing, m aintaining and m onitoring a business case are fundam ental and im portant disciplines for
justifying, supporting and then ensuring successful outcom es for any initiative, including im provem ent of the
governance system . T hey ensure a continuous focus on the benefits of the program  and their realization.
5.2 .2   P hase 2 — W here A re W e N ow ?
Phase 2  aligns I&T -related objectives w ith enterprise strategies and risk, and prioritizes the m ost im portant enterprise
goals, alignm ent goals and processes. T he C O BIT ® 2019 D esign G uide provides several design factors to help w ith
the selection.
B ased on the selected enterprise and IT -related goals and other design factors, the enterprise m ust identify critical
governance and m anagem ent objectives and underlying processes that are of sufficient capability to ensure
successful outcom es. M anagem ent needs to know  its current capability and w here deficiencies m ay exist. T his can
be achieved by a process capability assessm ent of the current status of the selected processes.
Figure 5.1— C O BIT Im plem entation R oadm ap
the momentum going?
7 How do we keep
6 Did we get there?
5 How do we get there?
4 What needs to be done?
3 Where do we want to be?
2 Where are we now?
1 What are the drivers?
• Program management
(outer ring)
• Chan ge enablement
(middle ring)
• Continual imp rovement life cycle
( i n n e r  r i n g )
Initiate program
Define problems and
opportunities
Define road map
Plan program
Execute plan
Realize benefits
Review
effectiveness
Operate
Identify role
Communicate
team
to change
and use
players
outcome
Form
implementation
Establish desire
Embed new

Sustain
approaches
Implement
improvements
state
Assess
RecognizeMonitor
Operate
improvements Build
target
current
need toand
and
Define
state
act
evaluate
measure

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

47

# C H A P TE R  5

C O N N E C TIN G  W ITH  TH E  CO BIT ® 2019 IM PLEM EN T A TIO N  G UID E
5.2 .3  P hase 3— W here Do W e W ant to B e?
Phase 3  sets a target for im provem ent follow ed by a gap analysis to identify potential solutions.
Som e solutions w ill be quick w ins and others m ore challenging, long-term  tasks. Priority should be given to projects
that are easier to achieve and likely to give the greatest benefit. Longer-term  tasks should be broken dow n into
m anageable pieces.
5.2 .4  P hase 4— W hat N eeds to B e Done?
Phase 4 describes how  to plan feasible and practical solutions by defining projects supported by justifiable business
cases and a change plan for im plem entation. A  w ell-developed business case can help ensure that the project’s
benefits are identified and continually m onitored.
5.2 .5  P hase 5— H ow  Do W e G et There?
Phase 5 provides for im plem enting the proposed solutions via day-to-day practices and establishing m easures and
m onitoring system s to ensure that business alignm ent is achieved, and perform ance can be m easured.
Success requires engagem ent, aw areness and com m unication, understanding and com m itm ent of top m anagem ent,
and ow nership by the affected business and IT  process ow ners.
5.2 .6   P hase 6 — Did W e G et There?
Phase 6 focuses on sustainable transition of the im proved governance and m anagem ent practices into norm al
business operations. It further focuses on m onitoring achievem ent of the im provem ents using the perform ance
m etrics and expected benefits.
5.2 .7  P hase 7— H ow  Do W e Keep the M om entum  G oing?
Phase 7 review s the overall success of the initiative, identifies further governance or m anagem ent requirem ents and
reinforces the need for continual im provem ent. It also prioritizes further opportunities to im prove the governance
system .
Program  and project m anagem ent is based on good practices and provides for checkpoints at each of the seven
phases to ensure that the program ’s perform ance is on track, the business case and risk are updated, and planning for
the next phase is adjusted as appropriate. It is assum ed that the enterprise’s standard approach w ould be follow ed.
F urther guidance on program  and project m anagem ent can also be found in C OB IT  m anagem ent objectives B A I01
M anaged program s and B A I11 M anaged projects . A lthough reporting is not m entioned explicitly in any of the
phases, it is a continual thread through all of the phases and iterations.
5.3  R elationship B etw een C O B IT D esign G uide and C O B IT Im plem entation G uide
T he C O BIT ® 2019 D esign G uide elaborates on a set of tasks defined in the C O BIT ® 2019 Im plem entation G uide .
Figure 5.2 describes the connection points betw een both G uides, and the purpose of this table is that users of the
C O BIT ® 2019 Im plem entation G uide find appropriate additional and m ore detailed guidance for certain phases and
activities in the C O BIT ® 2019 D esign G uide.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

48

Figure 5.2— C onnection P oints Betw een C O B IT D esign G uide and C O B IT Im plem entation G uide

## C O BIT Im plem entation G uide C O BIT Design G uide

Phase 1— W hat are the drivers?  (C ontinuous im provem ent [C I]
tasks)
Step 1— Understand the enterprise context and strategy.
1 Identify the current governance context, business IT and IT
pain points, events, and symptoms triggering the need to
act.
1.4 Understand current I&T-related issues.
2 Identify the business and governance drivers and
compliance requirements for improving the enterprise
governance of I&T (EGIT) and assess current stakeholder
needs.
1.1
1.2
1.3
Understand enterprise strategy.
Understand enterprise goals.
Understand the risk proﬁle.
3 Identify business priorities and business strategy dependent
on IT, including any current signiﬁcant projects.
1.1
1.2
1.3
Understand enterprise strategy.
Understand enterprise goals.
Understand the risk proﬁle.
4 Align with enterprise policies, strategies, guiding principles
and any ongoing governance initiatives.
Not exclusively governance design steps, these tasks are
more related to change enablement (CE) tasks in the
CO BIT Im plem entation G uide and are adequately covered
there.
5 Raise executive awareness of IT’s importance to the
enterprise and the value of EGIT.
6 Deﬁne EGIT policy, objectives, guiding principles and high-
level improvement targets.
7 Ensure that the executives and board understand and
approve the high-level approach, and accept the risk of not
taking any action on signiﬁcant issues.
Phase 2— W here are w e now ?  (C I tasks) Step 2— Determ ine the initial scope of the governance
system .
Step 3 — Reﬁne the scope of the governance system .
Step 4— C onclude the governance system  design.
1 Identify key enterprise and supporting IT-related goals. 2.1
2.2
Consider enterprise strategy.
Consider enterprise goals and apply the COBIT
goals cascade.
2 Establish the signiﬁcance and nature of IT’s contribution
(solutions and services) required to support business
objectives.
2.2
3 .3
3 .4
3 .5
3 .6
3 .7
Consider enterprise goals and apply the COBIT
goals cascade.
Consider the role of IT.
Consider the sourcing model.
Consider IT implementation methods.
Consider the technology adoption strategy.
Consider enterprise size.
3 Identify key governance issues and weaknesses related to
the current and required future solutions and services, the
enterprise architecture needed to support the IT-related
goals, and any constraints or limitations.
2.4 Consider current I&T-related issues.
4 Identify and select the processes critical to support IT-
related goals and, if appropriate, key management practices
for each selected process.
2.1
2.2
Consider enterprise strategy.
Consider enterprise goals and apply the COBIT
goals cascade.
5 Assess beneﬁt/value enablement risk, program/project
delivery risk and service delivery/IT operations risk related to
critical IT processes.
2.3 Consider the risk proﬁle of the enterprise.
6 Identify and select IT processes critical to ensure that risk is
avoided.
2.3 Consider the risk proﬁle of the enterprise.
7 Understand the risk acceptance position as deﬁned by
management.
1.3
2.3
Understand the risk proﬁle.
Consider the risk proﬁle of the enterprise.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

49

# C H A P TE R  5

C O N N E C TIN G  W ITH  TH E  CO BIT ® 2019 IM PLEM EN T A TIO N  G UID E
Figure 5.2— C onnection P oints Betw een C O B IT D esign G uide and C O B IT Im plem entation G uide (cont.)

## C O BIT Im plem entation G uide C O BIT Design G uide

Phase 2— W here are w e now ?  (C I tasks) Step 2— Determ ine the initial scope of the governance
system .
Step 3 — Reﬁne the scope of the governance system .
Step 4— C onclude the governance system  design.
8 Deﬁne the method for executing the assessment. The assessment method for processes is the method
described in the CO BIT ® 2019 Fram ew ork: Introduction
and M ethodology publication (based on CMMI capability
levels).
9 Document understanding of how the current process
actually addresses the management practices selected
earlier.
2.1
2.2
2.3
2.4
3 .1
3 .2
3 .3
3 .4
3 .5
3 .6
3 .7
Consider enterprise strategy.
Consider enterprise goals and apply the COBIT
goals cascade.
Consider the risk proﬁle of the enterprise.
Consider current I&T-related issues.
Consider the threat landscape.
Consider compliance requirements.
Consider the role of IT.
Consider the sourcing model.
Consider IT implementation methods.
Consider the technology adoption strategy.
Consider enterprise size.
10 Analyze the current level of capability. 4.1
4.2
Resolve inherent priority conﬂicts.
Conclude the governance system design.
11 Deﬁne the current process capability rating. 4.1
4.2
Resolve inherent priority conﬂicts.
Conclude the governance system design.
Phase 3 — W here do w e w ant to be?  (C I tasks) Step 4— C onclude the governance system  design.
1 Deﬁne targets for improvement:
Based on enterprise requirements for performance and 
conformance, decide the initial ideal short- and long-term
target capability levels for each process.
To the extent possible, benchmark internally to identify 
better practices that can be adopted.
To the extent possible, benchmark externally with 
competitors and peers to help decide the appropriateness
of the chosen target level.
Do a “sanity check” of the reasonableness of the targeted 
level (individually and as a whole), looking at what is
achievable and desirable and can have the greatest
positive impact within the chosen time frame.
4.1
4.2
Resolve inherent priority conﬂicts.
Conclude the governance system design.
2 Analyze gaps:
Use understanding of current capability (by attribute) and 
compare it to the target capability level.
Leverage existing strengths wherever possible to deal with 
gaps and seek guidance from COBIT management practices
and activities and other speciﬁc good practices and

## standards such as ITIL, International Organization for

## Standardization/International Electrotechnical Commission

## (ISO/IEC) 27000, The Open Group Architectural Framework

## (TOGAF ®) and the Project Management Body of Knowledge

(PMBOK ®), to close other gaps.
Look for patterns that indicate root causes to be addressed.
4.1
4.2
Resolve inherent priority conﬂicts.
Conclude the governance system design.
3 Identify potential improvements:
Collate gaps into potential improvements.
Identify unmitigated residual risk and ensure formal
acceptance.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

50
P age intentionally left blank

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

51

# C H A P TE R  6

# TH E  G O V E R N A N C E  SYSTE M  DE SIG N  TO O LK IT

P art II
E xecution and E xam ples
C hapter 6

## The G overnance S ystem  Design Toolkit

6.1  Introduction
T his chapter introduces the C O BIT D esign G uide com panion toolkit, an E xcel ® spreadsheet-based tool that facilitates
the application of the governance system  design w orkflow  explained in C hapter 4.
T he toolkit w as used to illustrate the three exam ples outlined in C hapter 7 of this publication. T his introduction
should help readers obtain a basic understanding of the toolkit, and appreciate how  the results w ere generated for
exam ples in C hapter 7. T he toolkit as dow nloaded show s the values illustrated in this chapter. T o use the tool, change
the values to fit the enterprise context.
N ote: M any m ethods exist to quantify and rank priorities for governance and m anagem ent objectives. In this
publication and its accom panying toolkit, one m ethod w as selected, but that does not exclude other valuable
m ethods that are capable of delivering reliable results.
6.2   T oolkit B asics
T he toolkit consists of an E xcel spreadsheet. T he spreadsheet contains:
A n introduction and instructions tab that provides basic inform ation about how  to use the toolkit 
A  canvas tab that consolidates all results of the governance system  design w orkflow 
One tab for each design factor (D F ), w here: 
Values can be entered and graphically represented 
Priority scores for governance and m anagem ent objectives are calculated and presented in table form at and 
graphically in tw o diagram s
T w o sum m ary tabs (one after Step 2  and another after Step 3  of the governance system  design w orkflow ) that 
graphically represent the outcom es of each com pleted step
M apping tables for design factors that have input values used by other tabs (these tables are hidden to increase the 
readability of the spreadsheet)
M apping tables (w ith the exception of  D esign F actor 2  Enterprise goals ) contain values betw een zero (0) and 
four (4), indicating the relevance of each governance/m anagem ent objective for each respective value of the
design factor, risk scenario or I&T -related issue.
A  value of 4 m eans m axim al relevance, w hile a value of 0 m eans no relevance. -
Values reflect averages that w ere established by an expert panel. T he values cannot, and do not, m odel every -
given individual situation, and should therefore be used w ith caution. T hey can, how ever, give good,
representative indications, and can be considered as directional guidance.
T he m apping table for D esign F actor 2  Enterprise goals is slightly different, in that it contains tw o m apping 
tables. One table m aps from  enterprise goals to alignm ent goals, and the other table m aps from  alignm ent goals
to governance and m anagem ent objectives (see A ppendices B  and C ) .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

52
6.3  Step 1 and Step 2 : Determ ine the Initial Scope of the G overnance System
In these steps of the governance design w orkflow , the strategy, goals, risk profile and I&T -related issues of the
enterprise are assessed. T he steps assess the first four design factors (as defined in C hapter 4) to determ ine their
im pact on the initial design of a governance system :
E nterprise strategy 1.
E nterprise goals (via the goals cascade) 2.
IT  risk profile 3.
I&T -related issues 4.
6.3.1  E nterprise Strategy (Design Factor 1)

Input  Each of the four possible values for the enterprise strategy design factor—growth/acquisition,
innovation/differentiation, cost leadership, client services/stability—must be rated between 1 (not
important) and 5 (most important).
It is recommended to maintain suﬃcient spread between values.
C alculation  The toolkit performs a matrix calculation of the entered values for Design Factor 1 Enterprise strategy 
with the mapping table for design factor 1, resulting in a score for each governance/management
objective.
The toolkit performs a second matrix calculation of a baseline set of values for design factor 1 with 
the mapping table for design factor 1, resulting in a baseline score for each governance/management
objective.
The toolkit then calculates a relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output section of this tab contains the calculated relative importance of each of the 40 COBIT ®
2019 governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Sample Input Graph Sample Output Graph

3
5
1
2
G row th/A cquisition
Innovation/D ifferentiation
C lient Service/Stability
C ost
Leadership

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

53

# C H A P TE R  6

# TH E  G O V E R N A N C E  SYSTE M  DE SIG N  TO O LK IT

6.3.2   E nterprise G oals and A pplying the C O B IT G oals C ascade (Design Factor 2 )

Input  Each of the thirteen enterprise goals must be rated between 1 (not important) and 5 (most 
important).
Using the generic enterprise goals, determine the most important goals for the enterprise. It is 
advisable to select the top three to ﬁve most important enterprise goals; too many high-priority goals
will lead to less meaningful goals cascade results.
It is recommended to maintain suﬃcient spread between values.
C alculation  The tool performs a double matrix calculation between (1) the rated enterprise goals and the mapping 
table between enterprise goals and IT alignment goals, and (2) the result of the ﬁrst matrix calculation
and the mapping table between IT alignment goals and governance/management objectives.
The tool performs a second set of matrix calculations of a baseline set of values for Design Factor 2 
Enterprise goals , resulting in a baseline score for each governance/management objective.
The tool then calculates the relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output section of this sheet contains the calculated relative importance of each of the 40 COBIT ®
2019 governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Sample Input Graph Sample Output Graph

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

54
6.3.3  R isk P roﬁle of the E nterprise (Design Factor 3)

Input  Each of the 19 risk categories contained in the risk proﬁle design factor must be rated as follows:
Impact of the risk should it occur, as a value between 1 (not important) and 5 (critical) 
Likelihood of the risk to occur, as a value between 1 (very unlikely) and 5 (very likely) 
The tool assigns a risk rating (very high, high, normal, low) to each risk category, based on the 
combination of the impact and likelihood ratings.
It is recommended to maintain suﬃcient spread between values.
C alculation  The tool performs a matrix calculation of the risk ratings with the mapping table for Design Factor 3 
Risk proﬁle , resulting in a score for each governance/management objective.
The tool performs a second matrix calculation of a baseline set of risk ratings for design factor 3 with 
the mapping table for design factor 3, resulting in a baseline score for each governance/management
objective.
The tool then calculates a relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output section of this tool contains the calculated relative importance of each of the 40 COBIT ®
2019 governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Sample Input Table Sample Output Graph

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

55

# C H A P TE R  6

# TH E  G O V E R N A N C E  SYSTE M  DE SIG N  TO O LK IT

6.3.4  C urrent I& T -R elated Issues of the E nterprise (Design Factor 4)

## Sample Input Table Sample Output Graph

/g1/g1 /g1 /g1 /g1
/g1 /g1 /g1/g1 /g1 /g1 /g1 /g1 /g1
/g10/g29/g32/g31/g34/g36/g17/g30/g19/g21
/g1/g49/g55/g47/g57/g50/g3/g17/g35/g21/g28/g25/g30/g21
/g1 /g12/g33/g1/g10/g37/g37/g39/g23
/g1 /g10/g37/g37/g39/g23
/g1 /g16/g23/g36/g27/g33/g39/g37/g1/g10/g37/g37/g39/g23
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g2/g21/g11/g17/g8/g12/g11 /g25/g22/g28/g26
/g1 /g6/g19/g10/g11/g21/g24/g22/g27/g29
/g1 /g3/g16/g17/g17/g11/g9/g19/g13/g16/g15/g1/g25/g22/g24/g28
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1
/g1/g1/g1
/g1
/g3/g39/g37/g27/g32/g23/g37/g37/g1/g22/g23/g34/g19/g36/g38/g31/g23/g32/g38/g37/g1/g27/g31/g34/g30/g23/g31/g23/g32/g38/g27/g32/g25/g1/g38/g26/g23/g27/g36/g1/g33/g41/g32/g1/g27/g32/g24/g33/g36/g31/g19/g38/g27/g33/g32/g1/g37/g33/g30/g39/g38/g27/g33/g32/g37/g1/g41/g27/g38/g26/g1/g30/g27/g38/g38/g30/g23/g1
/g33/g36/g1/g32/g33/g1/g27/g32/g40/g33/g30/g40/g23/g31/g23/g32/g38/g1/g33/g24/g1/g38/g26/g23/g1/g23/g32/g38/g23/g36/g34/g36/g27/g37/g23/g1/g10/g17/g1/g22/g23/g34/g19/g36/g38/g31/g23/g32/g38/g1/g51/g36/g23/g30/g19/g38/g23/g22/g1/g38/g33/g1/g23/g32/g22/g48/g39/g37/g23/g36/g1
/g21/g33/g31/g34/g39/g38/g27/g32/g25/g45/g1/g41/g26/g27/g21/g26/g1/g33/g24/g38/g23/g32/g1/g37/g38/g23/g31/g37/g1/g24/g36/g33/g31/g1/g22/g27/g37/g37/g19/g38/g27/g37/g24/g19/g21/g38/g27/g33/g32/g1/g41/g27/g38/g26/g1/g10/g17/g1/g37/g33/g30/g39/g38/g27/g33/g32/g37/g1/g19/g32/g22/g1
/g37/g23/g36/g40/g27/g21/g23/g37/g52
/g10/g25/g32/g33/g36/g19/g32/g21/g23/g1/g33/g24/g1/g19/g32/g22/g47/g33/g36/g1/g32/g33/g32/g21/g33/g31/g34/g30/g27/g19/g32/g21/g23/g1/g41/g27/g38/g26/g1/g34/g36/g27/g40/g19/g21/g43/g1/g36/g23/g25/g39/g30/g19/g38/g27/g33/g32/g37
/g10/g32/g19/g20/g27/g30/g27/g38/g43/g1/g38/g33/g1/g23/g42/g34/g30/g33/g27/g38/g1/g32/g23/g41/g1/g38/g23/g21/g26/g32/g33/g30/g33/g25/g27/g23/g37/g1/g33/g36/g1/g27/g32/g32/g33/g40/g19/g38/g23/g1/g39/g37/g27/g32/g25/g1/g10/g53/g17
/g10/g16/g47/g14/g21/g28/g17/g36/g21/g20/g1/g10/g35/g35/g37/g21
/g7/g36/g39/g37/g38/g36/g19/g38/g27/g33/g32/g1/g20/g23/g38/g41/g23/g23/g32/g1/g22/g27/g24/g24/g23/g36/g23/g32/g38/g1/g10/g17/g1/g23/g32/g38/g27/g38/g27/g23/g37/g1/g19/g21/g36/g33/g37/g37/g1/g38/g26/g23/g1/g33/g36/g25/g19/g32/g27/g44/g19/g38/g27/g33/g32/g1/g20/g23/g21/g19/g39/g37/g23/g1/g33/g24/g1/g19/g1
/g34/g23/g36/g21/g23/g34/g38/g27/g33/g32/g1/g33/g24/g1/g30/g33/g41/g1/g21/g33/g32/g38/g36/g27/g20/g39/g38/g27/g33/g32/g1/g38/g33/g1/g20/g39/g37/g27/g32/g23/g37/g37/g1/g40/g19/g30/g39/g23
/g7/g36/g39/g37/g38/g36/g19/g38/g27/g33/g32/g1/g20/g23/g38/g41/g23/g23/g32/g1/g20/g39/g37/g27/g32/g23/g37/g37/g1/g22/g23/g34/g19/g36/g38/g31/g23/g32/g38/g37/g1/g51/g27/g46/g23/g46/g45/g1/g38/g26/g23/g1/g10/g17/g1/g21/g39/g37/g38/g33/g31/g23/g36/g52/g1/g19/g32/g22/g1/g38/g26/g23/g1/g10/g17/g1
/g22/g23/g34/g19/g36/g38/g31/g23/g32/g38/g1/g20/g23/g21/g19/g39/g37/g23/g1/g33/g24/g1/g24/g19/g27/g30/g23/g22/g1/g27/g32/g27/g38/g27/g19/g38/g27/g40/g23/g37/g1/g33/g36/g1/g19/g1/g34/g23/g36/g21/g23/g34/g38/g27/g33/g32/g1/g33/g24/g1/g30/g33/g41/g1/g21/g33/g32/g38/g36/g27/g20/g39/g38/g27/g33/g32/g1/g38/g33/g1
/g20/g39/g37/g27/g32/g23/g37/g37/g1/g40/g19/g30/g39/g23
/g16/g27/g25/g32/g27/g24/g27/g21/g19/g32/g38/g1/g10/g17/g48/g36/g23/g30/g19/g38/g23/g22/g1/g27/g32/g21/g27/g22/g23/g32/g38/g37/g45/g1/g37/g39/g21/g26/g1/g19/g37/g1/g22/g19/g38/g19/g1/g30/g33/g37/g37/g45/g1/g37/g23/g21/g39/g36/g27/g38/g43/g1/g20/g36/g23/g19/g21/g26/g23/g37/g45/g1/g34/g36/g33/g28/g23/g21/g38/g1
/g24/g19/g27/g30/g39/g36/g23/g1/g19/g32/g22/g1/g19/g34/g34/g30/g27/g21/g19/g38/g27/g33/g32/g1/g23/g36/g36/g33/g36/g37/g45/g1/g30/g27/g32/g29/g23/g22/g1/g38/g33/g1/g10/g17
/g16/g23/g36/g40/g27/g21/g23/g1/g22/g23/g30/g27/g40/g23/g36/g43/g1/g34/g36/g33/g20/g30/g23/g31/g37/g1/g20/g43/g1/g38/g26/g23/g1/g10/g17/g1/g33/g39/g38/g37/g33/g39/g36/g21/g23/g36/g51/g37/g52/g1
/g7/g19/g27/g30/g39/g36/g23/g37/g1/g38/g33/g1/g31/g23/g23/g38/g1/g10/g17/g48/g36/g23/g30/g19/g38/g23/g22/g1/g36/g23/g25/g39/g30/g19/g38/g33/g36/g43/g1/g33/g36/g1/g21/g33/g32/g38/g36/g19/g21/g38/g39/g19/g30/g1/g36/g23/g35/g39/g27/g36/g23/g31/g23/g32/g38/g37/g1
/g15/g23/g25/g39/g30/g19/g36/g1/g19/g39/g22/g27/g38/g1/g24/g27/g32/g22/g27/g32/g25/g37/g1/g33/g36/g1/g33/g38/g26/g23/g36/g1/g19/g37/g37/g23/g37/g37/g31/g23/g32/g38/g1/g36/g23/g34/g33/g36/g38/g37/g1/g19/g20/g33/g39/g38/g1/g34/g33/g33/g36/g1/g10/g17/g1/g34/g23/g36/g24/g33/g36/g31/g19/g32/g21/g23/g1
/g33/g36/g1/g36/g23/g34/g33/g36/g38/g23/g22/g1/g10/g17/g1/g35/g39/g19/g30/g27/g38/g43/g1/g33/g36/g1/g37/g23/g36/g40/g27/g21/g23/g1/g34/g36/g33/g20/g30/g23/g31/g37
/g16/g39/g20/g37/g38/g19/g32/g38/g27/g19/g30/g1/g26/g27/g22/g22/g23/g32/g1/g19/g32/g22/g1/g36/g33/g25/g39/g23/g1/g10/g17/g1/g37/g34/g23/g32/g22/g27/g32/g25/g45/g1/g38/g26/g19/g38/g1/g27/g37/g45/g1/g10/g17/g1/g37/g34/g23/g32/g22/g27/g32/g25/g1/g20/g43/g1/g39/g37/g23/g36/g1
/g22/g23/g34/g19/g36/g38/g31/g23/g32/g38/g37/g1/g33/g39/g38/g37/g27/g22/g23/g1/g38/g26/g23/g1/g21/g33/g32/g38/g36/g33/g30/g1/g33/g24/g1/g38/g26/g23/g1/g32/g33/g36/g31/g19/g30/g1/g10/g17/g1/g27/g32/g40/g23/g37/g38/g31/g23/g32/g38/g1/g22/g23/g21/g27/g37/g27/g33/g32/g1
/g31/g23/g21/g26/g19/g32/g27/g37/g31/g37/g1/g19/g32/g22/g1/g19/g34/g34/g36/g33/g40/g23/g22/g1/g20/g39/g22/g25/g23/g38/g37
/g5/g39/g34/g30/g27/g21/g19/g38/g27/g33/g32/g37/g1/g33/g36/g1/g33/g40/g23/g36/g30/g19/g34/g37/g1/g20/g23/g38/g41/g23/g23/g32/g1/g40/g19/g36/g27/g33/g39/g37/g1/g27/g32/g27/g38/g27/g19/g38/g27/g40/g23/g37/g45/g1/g33/g36/g1/g33/g38/g26/g23/g36/g1/g24/g33/g36/g31/g37/g1/g33/g24/g1/g41/g19/g37/g38/g23/g22/g1
/g36/g23/g37/g33/g39/g36/g21/g23/g37
/g10/g32/g37/g39/g24/g24/g27/g21/g27/g23/g32/g38/g1/g10/g17/g1/g36/g23/g37/g33/g39/g36/g21/g23/g37/g45/g1/g37/g38/g19/g24/g24/g1/g41/g27/g38/g26/g1/g27/g32/g19/g22/g23/g35/g39/g19/g38/g23/g1/g37/g29/g27/g30/g30/g37/g1/g33/g36/g1/g37/g38/g19/g24/g24/g1
/g20/g39/g36/g32/g33/g39/g38/g47/g22/g27/g37/g37/g19/g38/g27/g37/g24/g19/g21/g38/g27/g33/g32
/g10/g17/g48/g23/g32/g19/g20/g30/g23/g22/g1/g21/g26/g19/g32/g25/g23/g37/g1/g33/g36/g1/g34/g36/g33/g28/g23/g21/g38/g37/g1/g24/g36/g23/g35/g39/g23/g32/g38/g30/g43/g1/g24/g19/g27/g30/g27/g32/g25/g1/g38/g33/g1/g31/g23/g23/g38/g1/g20/g39/g37/g27/g32/g23/g37/g37/g1/g32/g23/g23/g22/g37/g1/g19/g32/g22/g1
/g22/g23/g30/g27/g40/g23/g36/g23/g22/g1/g30/g19/g38/g23/g1/g33/g36/g1/g33/g40/g23/g36/g1/g20/g39/g22/g25/g23/g38
/g15/g23/g30/g39/g21/g38/g19/g32/g21/g23/g1/g20/g43/g1/g20/g33/g19/g36/g22/g1/g31/g23/g31/g20/g23/g36/g37/g45/g1/g23/g42/g23/g21/g39/g38/g27/g40/g23/g37/g1/g33/g36/g1/g37/g23/g32/g27/g33/g36/g1/g31/g19/g32/g19/g25/g23/g31/g23/g32/g38/g1/g38/g33/g1/g23/g32/g25/g19/g25/g23/g1/g41/g27/g38/g26/g1
/g10/g17/g45/g1/g33/g36/g1/g19/g1/g30/g19/g21/g29/g1/g33/g24/g1/g21/g33/g31/g31/g27/g38/g38/g23/g22/g1/g20/g39/g37/g27/g32/g23/g37/g37/g1/g37/g34/g33/g32/g37/g33/g36/g37/g26/g27/g34/g1/g24/g33/g36/g1/g10/g17
/g4/g33/g31/g34/g30/g23/g42/g1/g10/g17/g1/g33/g34/g23/g36/g19/g38/g27/g32/g25/g1/g31/g33/g22/g23/g30/g1/g19/g32/g22/g47/g33/g36/g1/g39/g32/g21/g30/g23/g19/g36/g1/g22/g23/g21/g27/g37/g27/g33/g32/g1/g31/g23/g21/g26/g19/g32/g27/g37/g31/g37/g1/g24/g33/g36/g1/g10/g17/g48/g36/g23/g30/g19/g38/g23/g22/g1
/g22/g23/g21/g27/g37/g27/g33/g32/g37
/g6/g42/g21/g23/g37/g37/g27/g40/g23/g30/g43/g1/g26/g27/g25/g26/g1/g21/g33/g37/g38/g1/g33/g24/g1/g10/g17
/g13/g20/g37/g38/g36/g39/g21/g38/g23/g22/g1/g33/g36/g1/g24/g19/g27/g30/g23/g22/g1/g27/g31/g34/g30/g23/g31/g23/g32/g38/g19/g38/g27/g33/g32/g1/g33/g24/g1/g32/g23/g41/g1/g27/g32/g27/g38/g27/g19/g38/g27/g40/g23/g37/g1/g33/g36/g1/g27/g32/g32/g33/g40/g19/g38/g27/g33/g32/g37/g1/g21/g19/g39/g37/g23/g22/g1
/g20/g43/g1/g38/g26/g23/g1/g21/g39/g36/g36/g23/g32/g38/g1/g10/g17/g1/g19/g36/g21/g26/g27/g38/g23/g21/g38/g39/g36/g23/g1/g19/g32/g22/g1/g37/g43/g37/g38/g23/g31/g37
/g8/g19/g34/g1/g20/g23/g38/g41/g23/g23/g32/g1/g20/g39/g37/g27/g32/g23/g37/g37/g1/g19/g32/g22/g1/g38/g23/g21/g26/g32/g27/g21/g19/g30/g1/g29/g32/g33/g41/g30/g23/g22/g25/g23/g45/g1/g41/g26/g27/g21/g26/g1/g30/g23/g19/g22/g37/g1/g38/g33/g1/g20/g39/g37/g27/g32/g23/g37/g37/g1/g39/g37/g23/g36/g37/g1
/g19/g32/g22/g1/g27/g32/g24/g33/g36/g31/g19/g38/g27/g33/g32/g1/g19/g32/g22/g47/g33/g36/g1/g38/g23/g21/g26/g32/g33/g30/g33/g25/g43/g1/g37/g34/g23/g21/g27/g19/g30/g27/g37/g38/g37/g1/g37/g34/g23/g19/g29/g27/g32/g25/g1/g22/g27/g24/g24/g23/g36/g23/g32/g38/g1/g30/g19/g32/g25/g39/g19/g25/g23/g37
/g15/g23/g25/g39/g30/g19/g36/g1/g27/g37/g37/g39/g23/g37/g1/g41/g27/g38/g26/g1/g22/g19/g38/g19/g1/g35/g39/g19/g30/g27/g38/g43/g1/g19/g32/g22/g1/g27/g32/g38/g23/g25/g36/g19/g38/g27/g33/g32/g1/g33/g24/g1/g22/g19/g38/g19/g1/g19/g21/g36/g33/g37/g37/g1/g40/g19/g36/g27/g33/g39/g37/g1/g37/g33/g39/g36/g21/g23/g37
/g9/g27/g25/g26/g1/g30/g23/g40/g23/g30/g1/g33/g24/g1/g23/g32/g22/g48/g39/g37/g23/g36/g1/g21/g33/g31/g34/g39/g38/g27/g32/g25/g45/g1/g21/g36/g23/g19/g38/g27/g32/g25/g1/g51/g19/g31/g33/g32/g25/g1/g33/g38/g26/g23/g36/g1/g34/g36/g33/g20/g30/g23/g31/g37/g52/g1/g19/g1/g30/g19/g21/g29/g1/g33/g24/g1
/g33/g40/g23/g36/g37/g27/g25/g26/g38/g1/g19/g32/g22/g1/g35/g39/g19/g30/g27/g38/g43/g1/g21/g33/g32/g38/g36/g33/g30/g1/g33/g40/g23/g36/g1/g38/g26/g23/g1/g19/g34/g34/g30/g27/g21/g19/g38/g27/g33/g32/g37/g1/g38/g26/g19/g38/g1/g19/g36/g23/g1/g20/g23/g27/g32/g25/g1/g22/g23/g40/g23/g30/g33/g34/g23/g22/g1
/g19/g32/g22/g1/g34/g39/g38/g1/g27/g32/g1/g33/g34/g23/g36/g19/g38/g27/g33/g32
/g1 /g1/g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1/g1/g1 /g1 /g1 /g1
/g1 /g1/g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1 /g1/g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1 /g1/g1 /g1 /g1 /g1 /g1 /g1/g1
/g1 /g1/g1 /g1 /g1 /g1
/g1 /g1/g1 /g1 /g1 /g1
/g1/g1 /g1 /g1 /g1/g1 /g1
/g1/g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1 /g1/g1 /g1 /g1 /g1
/g1 /g1/g1 /g1 /g1 /g1/g1 /g1 /g1 /g1 /g1
/g1 /g1/g1 /g1 /g1/g1 /g1 /g1 /g1
/g1/g1 /g1 /g1 /g1 /g1/g1 /g1 /g1 /g1
/g1/g1/g1 /g1 /g1 /g1 /g1 /g1
/g1/g1 /g1/g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1 /g1/g1 /g1
/g1/g1/g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1/g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1/g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1
/g1/g1 /g1 /g1
/g1/g1 /g1 /g1/g1 /g1 /g1/g1 /g1
/g1/g1 /g1 /g1 /g1 /g1
/g1/g1 /g1 /g1/g1 /g1 /g1 /g1 /g1 /g1
/g1 /g1/g1 /g1 /g1 /g1 /g1
/g1 /g1/g1/g1 /g1 /g1 /g1 /g1/g1 /g1 /g1
/g1 /g1/g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1/g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1 /g1
/g1/g1 /g1 /g1 /g1 /g1 /g1
/g1/g1 /g1 /g1/g1 /g1 /g1 /g1 /g1 /g1/g1
/g1/g1/g1 /g1 /g1 /g1
/g1/g1/g1 /g1 /g1 /g1 /g1 /g1
/g1/g1 /g1 /g1
/g1/g1 /g1 /g1
/g1/g1 /g1 /g1
/g1/g1 /g1 /g1 /g1/g1 /g1 /g1
/g1/g1 /g1
Input  Each of the 20 I&T-related issues for the I&T-related issues design factor must be rated between 1 (no 
issue) and 3 (serious issue). Numbers 1, 2 or 3 should be keyed into the tool; the tool will then
automatically translate values into a symbol, based on the tool’s key for this rating.
It is recommended to maintain suﬃcient spread between values.
C alculation  The tool performs a matrix calculation of the entered values for Design Factor 4 I& T-Related Issues 
with the mapping table for design factor 4, resulting in a score for each governance/management
objective.
The tool performs a second matrix calculation of a baseline set of values for design factor 4 with the 
mapping table for design factor 4, resulting in a baseline score for each governance/management
objective.
The tool then calculates a relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output section of this tab contains the calculated relative importance of each of the 40 COBIT ®
2019 governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

56
6.3.5  C onclusion

Input  N/A 
C alculation  The tool performs a weighted summation of the calculated governance/management objectives 
importance scores related to the ﬁrst four design factors.
Weights can be entered on the canvas tab and are set to 1 by default. The weighting can be changed,
if, for example, the enterprise strategy is of greater importance than enterprise goals, risk or
I&T-related issues.
The achieved results are then normalized on a scale of 100 (both positive and negative) and reﬂected 
on the Step 2 summary tab.
The highest value (positive or negative) obtains a score of 100.
All other values are then prorated against this value.
The resulting list of scores not only provides a reliable view of the relative importance of all
governance/management objectives against each other, but also gives an indication of the absolute
importance. This output allows an enterprise not only to prioritize governance/management
objectives against each other, but also to deﬁne adequate target capability levels.
O utput  The Step 2 summary tab contains the calculated relative importance of each of the 40 COBIT ® 2019 
governance and management objectives.
The results are represented in table format (on the canvas tab), and as a bar chart (Step 2 summary 
tab)

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

57

## CHAPTER 6

# THE GOVERNANCE SYSTEM  DESIGN TOOLKIT

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

58
N ote: T he preceding sam ple graph is consistent w ith sam ple graphs for each design factor, in that it represents the
actual result, should design factors 1 through 4 be entered as show n in the sam ple inputs provided in this C hapter 6.
6.4  Step 3: R eﬁne the Scope of the G overnance System
In this step, the initial scope of the governance system  is further refined based on the assessm ent of the rem aining
design factors:
T hreat landscape 1.
C om pliance requirem ents 2.
R ole of IT 3.
Sourcing m odel for IT 4.
IT  im plem entation m ethods 5.
T echnology adoption strategy 6.
E nterprise size (note, this design factor is not included as part of the tool; see Section 6.4.7 for further detail) 7.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

59

# C H A P TER  6

# TH E G O V ER N A N C E SYSTEM  D ESIG N  TO O LK IT

6.4.1  Threat Landscape (D esign Factor 5)

Input  Each of the tw o possible values (high and norm al) for the threat landscape design factor m ust be 
rated betw een 0%  and 100% . The sum  of both values m ust be 100% .
For m any enterprises, 100%  w ill be assigned to one of the categories. The option is available to assign 
percentages w here a portion of enterprise operations is subject to a high threat landscape,  w hile
others are subject to a m ore norm al threat landscape.
C alculation  The tool perform s a m atrix calculation of the entered values for D esign Factor 5 T hreat landscape w ith 
the m apping table for design factor 5, resulting in a score for each governance/m anagem ent
objective.
The tool perform s a second m atrix calculation of a baseline set of values for design factor 5 w ith the 
m apping table for design factor 5, resulting in a baseline score for each governance/m anagem ent
objective.
The tool then calculates the relative im portance for each governance/m anagem ent objective as the 
relative difference betw een both sets of values, expressed as a percentage and rounded to 5. This
num ber can be positive or negative, indicating that a governance/m anagem ent objective is m ore or
less im portant w hen com pared to the baseline score.
O utput  The output of this tab contains the calculated relative im portance of each of the 40 C O BIT ® 2019 
governance and m anagem ent objectives.
The results are represented in table form at, as a bar chart and as a spider diagram . 
Sam ple Input G raph Sam ple O utput G raph
25%
75%

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

60
6.4.2   C om pliance R equirem ents (Design Factor 6 )

Input  Each of the three possible values for the compliance requirements design factor must be rated 
between 0% and 100%. The sum of all three values must be 100%.
For many enterprises, 100% will be assigned to one of the categories. However, the option is available 
to assign different percentages,  if the enterprise’s IT landscape is quite vast, and certain parts are
subject to strict compliance regulation, while other parts are subject to less strict regulation.
C alculation  The tool performs a matrix calculation of the entered values for Design Factor 6 Com pliance 
Requirem ents with the mapping table for design factor 6, resulting in a score for each
governance/management objective.
The tool performs a second matrix calculation of a baseline set of values for design factor 6 with the 
mapping table for design factor 6, resulting in a baseline score for each governance/management
objective.
The tool then calculates a relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output of this tab contains the calculated relative importance of each of the 40 COBIT ® 2019 
governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Sample Input Graph Sample Output Graph

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

61

# C H A P TE R  6

# TH E  G O V E R N A N C E  SYSTE M  DE SIG N  TO O LK IT

6.4.3  R ole of IT (Design Factor 7)

## Sample Input Graph Sample Output Graph

Input  Each of the four possible values for the role of IT design factor—support, factory, turnaround and 
strategic—must be rated between 1 (not important) and 5 (most important).
It is recommended to maintain suﬃcient spread between values.
C alculation  The tool performs a matrix calculation of the entered values for Design Factor 7 Role of IT with the 
mapping table for design factor 7, resulting in a score for each governance/management objective.
The tool performs a second matrix calculation of a baseline set of values for design factor 7 with the 
mapping table for design factor 7, resulting in a baseline score for each governance/management
objective.
The tool then calculates a relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output of this tab contains the calculated relative importance of each of the 40 COBIT ® 2019 
governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

62
6.4.4  Sourcing M odel for IT (Design Factor 8)

## Sample Input Graph Sample Output Graph

Input  Each of the three possible values for the sourcing model for IT design factor—outsourcing, cloud and 
insourcing—must be rated between 0% and 100%. The sum of all three values must be 100%.
Note that there is a fourth category—the hybrid classiﬁcation. This is not denoted in the tool, because,
by deﬁnition, assigning percentages to more than one of the other three values creates a hybrid
model.
C alculation  The tool performs a matrix calculation of the entered values for Design Factor 8 Sourcing M odel for IT 
with its corresponding mapping table, resulting in a score for each governance/management
objective.
The tool performs a second matrix calculation of a baseline set of values for design factor 8 with the 
mapping table for design factor 8, resulting in a baseline score for each governance/management
objective.
The tool then calculates a relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output section of this tab contains the calculated relative importance of each of the 40 COBIT ®
2019 governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

63

# C H A P TE R  6

# TH E  G O V E R N A N C E  SYSTE M  DE SIG N  TO O LK IT

6.4.5  IT Im plem entation M ethods (Design Factor 9)

Input  Each of the three possible values for the IT implementation methods design factor—Agile, DevOps 
and traditional—must be rated between 0% and 100%. The sum of all three values must be 100%.
Note that there is a fourth category—the hybrid classiﬁcation. This is not denoted in the tool, because,
by deﬁnition, assigning percentages to more than one of the other three values creates a hybrid
model.
C alculation  The tool performs a matrix calculation of the entered values for Design Factor 9 IT Im plem entation 
M ethods with the mapping table for design factor 9, resulting in a score for each
governance/management objective.
The tool performs a second matrix calculation of a baseline set of values for design factor 9 with the 
mapping table for design factor 9, resulting in a baseline score for each governance/management
objective.
The tool then calculates a relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output section of this tab contains the calculated relative importance of each of the 40 COBIT ®
2019 governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Sample Input Graph Sample Output Graph

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

64
6.4.6   T echnology A doption Strategy (Design Factor 10 )

Input  Each of the three possible values for the technology adoption strategy design factor—ﬁrst mover,
follower, slow adopter—must be rated between 0% and 100%. The sum of all three values must be
100%.
For many enterprises, 100% may be assigned to one of the categories. However, the option is 
available to assign different percentages, if the enterprise’s IT landscape is quite vast, and different
areas adopt technology at difference paces.
C alculation  The tool performs a matrix calculation of the entered values for Design Factor 10 Technology 
Adoption Strategy with the mapping table for design factor 10, resulting in a score for each
governance/management objective.
The tool performs a second matrix calculation of a baseline set of values for design factor 10 with the 
mapping table for design factor 10, resulting in a baseline score for each governance/management
objective.
The tool then calculates a relative importance for each governance/management objective as the 
relative difference between both sets of values, expressed as a percentage and rounded to 5. This
number can be positive or negative, indicating that a governance/management objective is more or
less important when compared to the baseline score.
O utput  The output of this tab contains the calculated relative importance of each of the 40 COBIT ® 2019 
governance and management objectives.
The results are represented in table format, as a bar chart and as a spider diagram.

## Sample Input Graph Sample Output Graph

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

65

# C H A P TE R  6

# TH E  G O V E R N A N C E  SYSTE M  DE SIG N  TO O LK IT

6.4.7  E nterprise Size (Design Factor 11)
T he enterprise size design factor only indicates w hether the sm all and m edium  enterprise focus area guidance should
be used, instead of the core C OB IT  guidance. 2 7
1 T he size of an enterprise has no im pact on the priority and target
capability levels of governance and m anagem ent objectives.
6.4.8  C onclusion

N ote: T he follow ing sam ple graph is consistent w ith sam ple graphs for each design factor, in that it represents the
actual result, should design factors 5 through 10 be entered as show n in the sam ple inputs provided in this C hapter 6.

1
2 7 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the sm all and m edium
enterprise focus area content w as in developm ent and not yet released.
Input  N/A 
C alculation  The tool performs a weighted summation of the calculated governance/management objectives 
importance scores related to the design factors 5 through 10, and combines it with the results of Step
2 Initial design of the governance system .
Weights can be entered on the canvas tab and are set to 1 by default. The weighting can be changed,
if, for example, compliance requirements are of greater importance (because the enterprise operates
in a highly regulated industry).
The achieved results are then normalized on a scale of 100.
The highest value (positive or negative) obtains a score of 100.
All other values are then prorated against this value.
The resulting list of scores not only provides a reliable view of the relative importance of all
governance/management objectives against each other, but also gives an indication of the absolute
importance. This output allows an enterprise not only to prioritize governance/management
objectives against each other, but also to deﬁne adequate target capability levels.
O utput  The Step 3 summary tab contains the calculated relative importance of each of the 40 COBIT ® 2019 
governance and management objectives.
The results are represented in table format (on the canvas tab) and as a bar chart (on the Step 3 
summary tab)

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# COBIT ® 2019 DESIGN GUIDE

66
Sam ple O utput G raph

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

67

# C H A P TE R  7

# E X A M P LE S

## Chapter 7

Exam ples
7.1  Introduction
In this chapter, the w orkflow  explained in C hapter 4 is applied to tw o fictitious exam ples and one case study, in order
to illustrate the governance system  design process. T he exam ples include:
M anufacturing enterprise (Section 7.2 ) 1.
M edium -sized innovative com pany (Section 7.3 ) 2.
H igh-profile governm ent agency (Section 7.4) 3.
7.2   E xam ple 1: M anufacturing E nterprise
T he corporation m anufactures goods, is a large enterprise, is very cost conscious,  and desires to be a cost leader in
its m arket. T he enterprise considers I&T  purely a supporting function for efficient and effective operations. A lthough
IT  is a supporting function, the enterprise is critically dependent on it. T he enterprise takes a traditional approach to
new  developm ent and operations, and is quite hesitant to adopt new  technologies. R ecently, the enterprise w as
confronted w ith a m alw are attack and suffered from  a num ber of operational IT  problem s. T he enterprise houses and
operates critical IT  equipm ent in-house.
7.2 .1  Step 1: U nderstand the E nterprise C ontext and Strategy
T he first step of the governance design w orkflow  is to sum m arize the external and internal context of the enterprise.
Step 1.1: U nderstand enterprise strategy — A  prim ary focus on cost leadership and a secondary focus on client
service/stability are depicted in figure 7 .1 .

Figure 7 .1— Exam ple 1, Step 1.1: Enterprise Strategy
Client Ser vice/Stability
Design F act or 1 Enterprise Str ategy
Impor tance of Diff erent Strategies (Input)
0
1
1
5
3
1 2 34 5

## Cost Leadership

Inno vation/Differentiation
Growth/Acquisition

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

68
Step 1.2 : U nderstand enterprise goals — T he enterprise has ranked the 13  generic enterprise goals on a scale from  1 to
5, as depicted in the follow ing diagram . Figure 7 .2 show s that E G 09  O ptim ization of business process costs is the
highest-ranked enterprise goal.

Figure 7 .2— Exam ple 1, Step 1.2: Enterprise G oals
EG01— P ortfolio of competitive products and services
EG0 2— Mana ged business risk
EG03— Compliance with external laws and r egulations
EG04— Quality of financial information
EG05— Cust omer-oriented ser vice cultur e
EG0 6— Busi ness-service continuity and availability
EG07— Quality of management information
EG08— Optimization of internal business pr ocess functionality
EG09— Optimization of business pr ocess costs
EG10— Staff skills, motiv ation and pr oductivity
EG11— Compliance with internal policies
EG12— Managed digital tr ansformation pr ogr ams
EG13— Pr oduct and business inno vation

## Design F act or 2 Enterprise Goals

5
5
2
2
2
3
3
3
4
4
4
4
1
1
1

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

69

# C H A P TE R  7

# E X A M P LE S

Step 1.3 : U nderstand the risk profile — A  high-level risk analysis has resulted in a risk profile, identifying the
follow ing highest risk categories (m arked w ith red dots in the risk-rating colum n in figure 7 .3 ): IT  operational
infrastructure incidents, unauthorized actions, softw are adoption/usage problem s, hardw are incidents, softw are
failures and logical attacks. (T hese are broad categories. F or detailed exam ples of risk scenarios w ithin each
category, please see Section 2 .6.)

Figure 7 .3 — Exam ple 1, Step 1.3 : R isk P rofile

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

70
Step 1.4: U nderstand current I&T -related issues — A n analysis of the current situation (on a scale from  1 to 3 )
resulted in an assessm ent of current I&T -related issues, as depicted in figure 7 .4 . T hese are perceived to be im portant
issues to the enterprise: significant incidents, service delivery problem s by outsourcers, hidden IT  cost and IT  cost
overall.

Figure 7 .4— Exam ple 1, Step 1.4: I&T- R elated Issues

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

71

# C H A P TE R  7

# E X A M P LE S

7.2 .2   Step 2 : Determ ine the Initial Scope of the G overnance System
T he initial scope of the governance system  is determ ined by using the inform ation (partial or in full) collected during
Step 1. Step 2  translates this inform ation on enterprise goals, enterprise strategy and risk profile to relevant
governance com ponents.
Step 2 .1: C onsider enterprise strategy — Figure 7 .5 represents the enterprise strategy, as identified in step 1.1. Figure
7 .6 show s the relative influence these strategies have on governance and m anagem ent objectives .

Figure 7 .5— Exam ple 1, Step 2.1: Enterprise Strategy
Client Ser vice/Stability
Design F act or 1 Enterprise Str ategy
Impor tance of Diff erent Strategies (Input)
0
1
1
5
3
1 2 34 5

## Cost Leadership

Inno vation/Differentiation
Growth/Acquisition

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

72

In addition to the governance and m anagem ent processes highlighted by figure 7 .6 , the follow ing other com ponents
also require attention require attention:
F ocus on IT  costing and budgeting skills 
Influence of the culture and behavior com ponent 
C ontribution of the services, infrastructure and applications com ponent (e.g., for autom ation of controls, im proving 
efficiency)
Figure 7 .6 — Exam ple 1, Step 2.1: R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 1 Enterprise Strategy

Design F act or 1 Enterprise Str ategy
Resulting Go vernance/Management Objectives Importance (Output)
100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

73

# C H A P TE R  7

# E X A M P LE S

Step 2 .2 : C onsider enterprise goals and apply the C OB IT  goals cascade — A t this point, the C OB IT  goals cascade is
applied to determ ine w hich governance and m anagem ent objectives are relevant to achieve the priority enterprise
goals, based on their ranking, assigned in step 1.2  ( figure 7 .7 ). Figure 7 .8 show s the relative influence these ranked
enterprise goals have on governance and m anagem ent objectives.

Figure 7 .7 — Exam ple 1, Step 2.2: Enterprise G oals
EG01— P ortfolio of competitive products and services
EG02— Managed business risks
EG03— Compliance with external laws and r egulations
EG04— Quality of financial information
EG05— Cust omer-oriented ser vice cultur e
EG06— Business ser vice continuity and a vailability
EG07— Quality of management information
EG08— Optimization of internal business pr ocess functionality
EG09— Optimization of business pr ocess costs
EG010— Staff skills, motiv ation and pr oductivity
EG011— Compliance with internal policies
EG012— Managed digital tr ansformation pr ogr ams
EG013— Pr oduct and business inno vation

## Design F act or 2 Enterprise Goals

5
5
2
2
2
3
3
3
4
4
4
4
1
1
1

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

74

Figure 7 .8— Exam ple 1, Step 2.2: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 2 Enterprise G oals

## Design F act or 2 Enterprise Goals

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

75

# C H A P TE R  7

# E X A M P LE S

Step 2 .3 : C onsider the risk profile of the enterprise — In step 1.3 , the IT  risk categories w ere identified and analyzed
at a high level ( figure 7 .9 ). B ased on the m apping betw een the risk profile and the C OB IT  governance and
m anagem ent objectives (as explained in Section 4.2 .3 , and per the m apping table included in A ppendix D ),
figure 7 .10 show s the relative ranking of the governance and m anagem ent objectives, based on the results of the
risk analysis.

Figure 7 .9 — Exam ple 1, Step 2.3 : R isk P rofile

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

76

Figure 7 .10— Exam ple 1, Step 2.3 : R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 3  R isk P rofile
Design F act or 3 Risk Pr ofile

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

77

# C H A P TE R  7

# E X A M P LE S

Step 2 .4: C onsider current I&T -related issues— In this step, the issues identified in step 1.4 are related to the C OB IT
governance and m anagem ent objectives through a m apping table ( A ppendix E ) that associates each issue to one or
m ore governance or m anagem ent objectives that can influence that issue. B ased on that m apping (as explained in
Section 4.2 .4), figure 7 .12 show s the relative ranking of the governance and m anagem ent objectives, based on the
enterprise’s analysis of current I&T -related issues (figure 7 .11) .

Figure 7 .11— Exam ple 1, Step 2.4: I&T- R elated Issues

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

78

Figure 7 .12— Exam ple 1, Step 2.4: R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 4 I& T-R elated Issues

Design F act or 4 I&T -Related Issues

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

79

# C H A P TE R  7

# E X A M P LE S

Step 2 .5: Initial scope of the governance system — A t this point, it is possible to com bine the resulting governance
and m anagem ent priorities from  the previous four steps to produce the follow ing initial priorities for governance and
m anagem ent objectives in the governance system  ( figure 7 .13 ).

T he top five follow ing m anagem ent objectives are likely to be im portant for the governance system  of this
enterprise:

## B A I09  M anaged Assets 

## D SS02  M anaged Service Requests and Incidents 

D SS03  M anaged Problem s 
B A I10 M anaged C onfiguration 
A PO12  M anaged Risk 
T he follow ing m anagem ent objectives seem  (for now ) the least im portant:
A PO04 M anaged Innovation 
Figure 7 .13 — Exam ple 1, Step 2.5: Initial Design Sum m ary of G overnance and M anagem ent
O bjectives Im portance
-15
-25
-25
-75
-30
-10
-10
-40
-40
-25
-25
-10
-60
5
0
0
0
0
0
0
0
0
30
30
25
55
45
25
25
30
100
60
40
70
60
45
45
15
15
10
-100 -50

# EDM01

# EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO03

# APO04

# APO05

# APO06

# APO07

# APO08

# APO02

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01

# BAI02

# BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO09

05 0 100
Step 2 Initial Design (Summar y)

## Governance and Management Objectives Importance

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

80

## B A I11 M anaged Projects 

A PO02  M anaged Strategy 
B A I01 M anaged Program s 
A PO05 M anaged Portfolio 
T he next step w ill determ ine w hich refinem ents are still required to this initial scope of the governance system .
7.2 .3  Step 3: R eﬁne the Scope of the G overnance System
In step 3 , refinem ents to the initial scope are identified, based on the rem aining set of design factors to be analyzed. N ot all
design factors m ight be applicable for each enterprise, in w hich case they can be ignored. Figure 7 .14 show s a sum m ary of
the design factors 5 through 11 that are applicable to the m anufacturing enterprise in this exam ple. W hen m ore than one
value w as applicable for a certain design factor, it is so indicated in the value colum n of the figure.

1
2 8 T his figure m eans that 9 0% of the enterprise’s operations and I&T  activities are done in a high threat landscape.
2
2 9 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the inform ation
security focus area content w as in developm ent and not yet released.
3
3 0 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the inform ation
security focus area content w as in developm ent and not yet released.
4
3 1 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the D evOps focus
area content w as in developm ent and not yet released.
Figure 7 .14— Exam ple 1 Tailored V ersion of G overnance System

## Ref Design Factor Value G overnance and M anagem ent

O bjectives Priority C om ponents Focus A rea
G uidance

## DF5 Threat Landscape

High 90% 28
1
Important governance and
management objectives include:

# EDM01, EDM03 

# APO01, APO03,  APO10, APO12,

# APO13, APO14

# BAI06, BAI10 

# DSS02, DSS04, DSS05, DSS06 

# MEA01, MEA03, MEA04 

Important organizational
structures include:
Security strategy 
committee

# CISO 

Important culture and
behavior aspects include:
Security awareness 
Information ﬂows:
Security policy 
Security strategy 
Information security
focus area 29
2
Normal 10%  As per the initial scope deﬁnition   N /A  COBIT core model
DF6 C om pliance Requirem ents
Normal 75%
Most important, but yet moderate,
management objectives include:

# EDM01, EDM03 

# APO12 

# MEA03 

N /A  COBIT core model
Low 25%  As per the initial scope deﬁnition   N /A  COBIT core model

## DF7 Role of IT

Factory
5 on
scale
of 5
Important governance and
management objectives include:

# EDM03 

# DSS01, DSS02, DSS03, DSS04 

N /A  Information security
focus area 30
3
Turnaround
2 on
scale
of 5
Important governance and
management objectives include:

# APO02, APO04 

# BAI02, BAI03 

N /A  DevOps focus area 31
4

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

81

# C H A P TE R  7

# E X A M P LE S

F or each design factor in figure 7 .14 , the current assessed situation can be com bined w ith the m apped governance
and m anagem ent objectives and other guidance in figure 7 .14 . T he follow ing exam ples w ere produced using m atrix
calculations betw een the input values and a m apping betw een these values and governance and m anagem ent
objectives. M apping tables are included in A ppendices F  through K  of this publication. T he resulting spider charts,
w ith the prioritized governance and m anagem ent objectives, represent relative im portance levels com pared to a
baseline level. R elative im portance levels are expressed on a scale from  -100 to +100, w ith zero (0) indicating that
there is no im pact on the im portance of a governance or m anagem ent objective, and +100 indicating that the
objective has becom e tw ice as im portant due to the design factor at hand.
5
3 2 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the vendor
m anagem ent focus area content w as being contem plated as a potential future focus area.
6
3 3 T his figure m eans that the organization is 9 0% considered to be a follow er in term s of technology adoption.
7
3 4 T his figure m eans that 10% of the enterprise’s I&T  activities are considered to be at a slow  adopter pace.
Figure 7 .14— Exam ple 1 Tailored V ersion of G overnance System (cont.)

## Ref Design Factor Value G overnance and M anagem ent

O bjectives Priority C om ponents Focus A rea
G uidance

## DF8 Sourcing M odel for IT

Outsourcing 20%
Important management objectives
include:

# APO09, APO10 

# MEA01 

N /A  Vendor management
focus area 32
5
Insourced 80%  As per the initial scope deﬁnition   N /A  COBIT core model
DF9 IT Im plem entation M ethods
Traditional  As per the initial scope deﬁnition   N /A  COBIT core model

## DF10 Technology A doption Strategy

Follower 90% 33
6
Important governance and
management objectives include:

# APO02, APO04 

# BAI01 

Processes that can run at a
slower pace
COBIT core model
Slow Adopter 10% 34
7  As per the initial scope deﬁnition   N /A  COBIT core model

## DF11 Enterprise Size

Large  As per the initial scope deﬁnition   N /A  COBIT core model

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

82
Step 3 .1— C onsider the threat landscape — Figure 7 .15 depicts the threat landscape under w hich the enterprise
believes it operates. Figure 7 .16 show s the im pact on governance and m anagem ent objectives of the assessed threat
landscape.

Figure 7 .15— Exam ple 1, Step 3 .1: Threat Landscape
Figure 7 .16 — Exam ple 1, Step 3 .1: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 5 T hreat Landscape
Design F act or 5 Thr eat Landscape
90%
10%

## Normal High

Design F act or 5 Thr eat Landscape

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

83

# C H A P TE R  7

# E X A M P LE S

T his classification of the threat landscape renders a substantial num ber of governance and m anagem ent objectives
m ore im portant, per the figure 7 .14 entry related to high-threat landscape. G uidance on these governance and
m anagem ent objectives should be draw n from  the inform ation security focus area guidance, 3 5
8 w hich contains m ore
detailed and specific guidance on inform ation security than the C OB IT  core m odel.
In addition, the enterprise m ust consider (for inclusion in its governance system  design) the presence and
perform ance of the follow ing:
Im portant organizational structures, including: 
Security strategy com m ittee 

# C ISO 

Im portant culture and behavior aspects, including: 
Security aw areness 
Inform ation flow s: 
Security policy 
Security strategy 
Step 3 .2 — C onsider com pliance requirem ents — Figure 7 .17 depicts the com pliance requirem ents for the enterprise,
w hich are estim ated to be norm al, leaning to low . Figure 7 .18 show s the im pact of the assessed com pliance
requirem ents on the governance and m anagem ent objectives. T here is very little im pact, w hich is the expected result.

8
3 5 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the inform ation
security focus area content w as in developm ent and not yet released.
Figure 7 .17 — Exam ple 1, Step 3 .2: C om pliance R equirem ents
Design F act or 6 Compliance Requir ements
75%
25%

## Normal Low High

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

84

Step 3 .3 — C onsider the role of IT — Figure 7 .19 show s the role of IT , w hich is expressed as factory, w ith a secondary
choice of turnaround, indicating that the enterprise is highly operationally dependent on its IT  services. Figure 7 .20
show s the im pact of the assessed role of IT  on the governance and m anagem ent objectives.

Figure 7 .18— Exam ple 1, Step 3 .2: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 6  C om pliance R equirem ents
Design F act or 6 Compliance Requir ements

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

Figure 7 .19 — Exam ple 1, Step 3 .3 : R ole of IT
Str ategic

## Design F act or 7 Role of I T

0
0
0
2
5
1 2 34 5
Turnaround
Factory
Suppor t

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

85

# C H A P TE R  7

# E X A M P LE S

In addition to the prioritized governance and m anagem ent objectives, guidance should be draw n from  the
inform ation security and D evOps focus areas (w hen available and necessary).
Figure 7 .20— Exam ple 1, Step 3 .3 : R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 7  R ole of IT

## Design F act or 7 Role of I T

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

86
Step 3 .4— C onsider the sourcing m odel— Figure 7 .21 depicts the selected sourcing m odel of the enterprise, w hich is
predom inantly insourcing. Figure 7 .22 show s the im pact of the assessed sourcing m odel on the  governance and
m anagem ent objectives. T he im pact is quite lim ited for this design factor.

Figure 7 .21— Exam ple 1, Step 3 .4: Sourcing M odel for IT
Figure 7 .22— Exam ple 1, Step 3 .4: R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 8 Sourcing M odel for IT

## Design F act or 8 Sour cing Model for I T

80%
20%
Cloud Insour cing Outsour cing

## Design F act or 8 Sour cing Model for I T

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

87

# C H A P TE R  7

# E X A M P LE S

Step 3 .5— C onsider IT  im plem entation m ethods— T he enterprise uses traditional IT  developm ent and operations
m ethods ( figure 7 .23 ), leading to no im pact on the governance and m anagem ent objectives ( figure 7 .24 ).

Figure 7 .23 — Exam ple 1, Step 3 .5: IT Im plem entation M ethods
Figure 7 .24— Exam ple 1, Step 3 .5: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 9  IT Im plem entation M ethods

## Design F act or 9 IT Implementation Methods

100%

## DevOps TraditionalAgile

## Design F act or 9 IT Implementation Methods

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

88
Step 3 .6— C onsider the technology adoption strategy— Figure 7 .25 indicates that the enterprise is, at best, a follow er
w hen it com es to new  technology adoption. Figure 7 .26 show s the very lim ited im pact this has on governance and
m anagem ent objectives priorities.

Figure 7 .25— Exam ple 1, Step 3 .6 : Technology A doption  Strategy

## Design F act or 10 Technology Adoption Strategy

90%
10%

## Follower Slow Adopter First Mo ver

Figure 7 .26 — Exam ple 1, Step 3 .6 : R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 10 Technology A doption Strategy

## Design F act or 10 Technology Adoption Strategy

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

89

# C H A P TE R  7

# E X A M P LE S

Step 3 .7— C onsider E nterprise Size — T he enterprise is classified as large. Per figure 7 .14 , this m eans that the
C OB IT  core m odel should be used as the basis for the definition of the governance system .
7.2 .4  Step 4: C onclude the G overnance Solution Design
T he last step in the design process requires all inputs from  previous steps to be discussed, conflicts resolved and a
conclusion reached. T he resulting governance system  reflects careful consideration of all inputs, taking into account
that these inputs w ere som etim es conflicting, and choices had to be m ade.
7.2 .4.1  G overnance and M anagem ent O bjectives
A t this point, it is possible to add the governance and m anagem ent priorities resulting from  steps 3 .1 through 3 .7 to
the results obtained from  the initial governance system  design in steps 2 .1 through 2 .4. T his synthesis results in the
follow ing adjusted priorities for governance and m anagem ent objectives in the governance system  (figure 7 .27 ) .

Figure 7 .27 — Exam ple 1, Step 4: G overnance and M anagem ent O bjectives Im portance (A ll Design
Factors)
-35
-5
-45
-5
-75
-40
-20
-50
-30
-30
-45
-20
-70
30
5
5
15
45
30
40
70
80
45
15
55
75
75
40
100
75
80
35
70
25
25
25

# EDM01

# EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO03

# APO04

# APO05

# APO06

# APO07

# APO08

# APO02

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01

# BAI02

# BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

0
0
0
0

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO09

-100 -50 05 0 100

## Governance and Management Objectives Importance (All Design Factors)

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

90
T he follow ing m anagem ent objectives are likely to be im portant for the governance system  of this enterprise:
D SS02  M anaged service requests and incidents (100) 
A PO13  M anaged security (80) 
D SS04 M anaged continuity (80) 
D SS03  M anaged problem s (75) 
B A I09  M anaged assets (75) 
B A I10 M anaged configuration (75) 
T he m ost im portant objectives have changed slightly com pared to the list identified in the initial scope definition in
step 2 .5. Som e governance/m anagem ent objectives have changed places, one dropped (A PO12 ), and tw o w ere added
(D SS04 and A PO13 ).
T he follow ing m anagem ent objectives seem  the least im portant:
A PO04 M anaged innovation 
B A I11 M anaged projects 
B A I01 M anaged program s 
A PO02  M anaged strategy 
B A I05 M anaged organizational change 
C om pared to the m ost im portant objectives, this list of the least im portant objectives changed even less from  the list
identified in the initial scope definition in step 2 .5. T his proves both that the initial scoping, based on the
fundam ental design factors, w as already quite accurate, and also that accounting for other design factors resulted in
additional adjustm ents.
In its discussions, the enterprise decides that the autom atically generated im portance values for som e
governance/m anagem ent objectives are not w hat they should be, and m akes the follow ing adjustm ents:
A PO06 M anaged budget and cost : +75 
E D M 04 Ensured resource optim ization : +75 
D SS02  M anaged service requests and incidents : -2 5 
In conclusion, the enterprise decides that the first stage of its governance system  design w ill consist of the
governance and m anagem ent objectives (w ith the underlying processes) show n in figure 7 .28 .

Figure 7 .28— Exam ple 1, G overnance and M anagem ent O bjectives and Target Process C apability Levels
Reference G overnance/M anagem ent O bjective Target Process
C apability Level
EDM 03 Ensured risk optimization 2
EDM 04 Ensured resource optimization 3
A PO 06 Managed budget and costs 4
A PO 09 Managed service level agreements 2
A PO 10 Managed vendors 2
A PO 11 Managed quality 2
A PO 12 Managed risk 3
A PO 13 Managed security 4
A PO 14 Managed data 2

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

91

# C H A P TE R  7

# E X A M P LE S

Figure 7 .28 show s the reference, governance or m anagem ent objective title, and the target capability level at w hich
the related processes should be im plem ented. G iven the high im portance of a num ber of processes, the target
capability level has been set at a higher value (3  or 4). T he logic applied by the enterprise w as that:
A ny governance/m anagem ent objective that scored 75 or higher— m eaning that its im portance w as at least 75% 
higher com pared to a benchm ark situation— w ould require a capability level 4.
A ny governance/m anagem ent objective that scored 50 or higher w ould require a capability level 3 . 
A ny governance/m anagem ent objective that scored 2 5 or higher w ould require a capability level 2 . 
It is reasonable to consider that the rem aining processes should reach capability level 1.
7.2 .4.2    O ther C om ponents
T he enterprise w ill need to pay specific attention to a strong im plem entation of the follow ing roles and structures:
Security strategy com m ittee 

# C ISO 

T he enterprise w ill also ensure adequate security aw areness throughout the enterprise, and im plem ent im portant
inform ation item s and flow s (security policy and security strategy).
7.2 .4.3  S pecific Focus A rea G uidance
T he enterprise w ill use the follow ing guidance to com plem ent the C OB IT  core m odel:
Inform ation security focus area 3 6
9 guidance, given the high threat landscape and the results of the risk analysis and 
the current I&T -related issues
D evOps and vendor m anagem ent focus area 3 7
10 guidance, w hen and w here applicable 
9
3 6 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the inform ation
security focus area content w as in developm ent and not yet released.
10
3 7 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the D evOps focus
area content w as in developm ent and not yet released, and the vendor m anagem ent focus area is being contem plated as a potential future focus area.
Figure 7 .28— Exam ple 1, G overnance and M anagem ent O bjectives and Target Process
C apability Levels (cont.)
Reference G overnance/M anagem ent O bjective Target Process
C apability Level
BA I06 Managed IT changes 3
BA I09 Managed assets 4
BA I10 Managed conﬁguration 4
DSS01 Managed operations 2
DSS02 Managed service requests and incidents 4
DSS03 Managed problems 4
DSS04 Managed continuity 4
DSS05 Managed security services 3
DSS06 Managed business process controls 2
M EA 02 Managed system of internal control 2
M EA 03 Managed compliance with external requirements 2
M EA 04 Managed assurance 2

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

92
7.3  E xam ple 2 : M edium -Sized Innovative C om pany
T his exam ple concerns a m edium -sized innovative com pany, developing appliances for the autom otive sector. T he
enterprise is relatively sm all, and its claim  to fam e is its fast innovation. It is critically dependent on IT  for both
product developm ent and m anufacturing of appliances. T he enterprise is both a user and a developer of softw are. It is
very eager to benefit from  every new ly available technology, and it is investing in a D evOps approach w herever
possible. It has m ade a strategic choice to outsource all infrastructure-related IT  services and go to the cloud.
7.3.1  Step 1: U nderstand the E nterprise C ontext and Strategy
T he first step of the governance design w orkflow  is to sum m arize the external and internal context of the enterprise.
Step 1.1: U nderstand enterprise strategy — A  prim ary focus on innovation and differentiation and a secondary
focuson grow th/acquisition are depicted in figure 7 .29 .

Figure 7 .29 — Exam ple 2, Step 1.1: Enterprise Strategy
Client Ser vice/Stability
Impor tance of Diff erent Strategies (Input)
Design F act or 1
0
3
5
2
2
1 2 34 5

## Cost Leadership

Inno vation/Differentiation
Growth/Acquisition

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

93

# C H A P TE R  7

# E X A M P LE S

Step 1.2 : U nderstand enterprise goals — T he enterprise has ranked the 13  generic enterprise goals on a scale from  1 to
5, as depicted in figure 7 .30 . T he diagram  show s that E G 01 Portfolio of com petitive products and services and E G 13
Product and business innovation are the highest-ranked enterprise goals.

Figure 7 .3 0— Exam ple 2, Step 1.2: Enterprise G oals
EG0 1— P ortfolio of competitive products and services
EG02— Managed business risk
EG03— Compliance with external laws and r egulations
EG04— Quality of financial information
EG05— Cust omer-oriented ser vice cultur e
EG06— Business-ser vice continuity and a vailability
EG07— Quality of management information
EG08— Optimization of internal business pr ocess functionality
EG09— Optimization of business pr ocess costs
EG10— Staff skills, motiv ation and pr oductivity
EG11— Compliance with internal policies
EG12— Managed digital tr ansformation pr ogr ams
EG13— Pr oduct and business inno vation
5
5
2
2
2
2
2
2
4
4
3
3
3

## Design F act or 2 Enterprise Goals

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

94
Step 1.3 : U nderstand the risk profile — A  high-level risk analysis resulted in a risk profile, identifying the highest risk
categories (m arked w ith red dots in the risk-rating colum n in figure 7 .31 : IT  investm ent decision m aking, portfolio
definition and m aintenance; IT  expertise, skills and behavior; and technology-based innovation. (T hese are broad
categories. F or detailed exam ples of risk scenarios w ithin each category, please see Section 2 .6.)

Figure 7 .3 1— Exam ple 2, Step 1.3 : R isk P rofile

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

95

# C H A P TE R  7

# E X A M P LE S

Step 1.4: U nderstand current I&T -related issues — A n analysis of the current situation (on a scale of im portance from
1 to 3 ) resulted in an assessm ent of current I&T -related issues, as depicted in figure 7 .32 . T he follow ing are
perceived to be im portant issues to the enterprise: insufficient IT  resources, IT  architecture and data quality issues.

Figure 7 .3 2— Exam ple 2, Step 1.4: I&T- R elated Issues

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

96
7.3.2   Step 2 : Determ ine the Initial Scope of the G overnance System
T he initial scope of the governance system  is determ ined by using the inform ation (partial or in full) collected during
Step 1. Step 2  translates this inform ation on enterprise strategy, enterprise goals, risk profile and I&T -related issues
into relevant governance com ponents.
Step 2 .1: C onsider enterprise strategy — Figure 7 .33 represents the enterprise strategy, as identified in step 1.1.
Figure 7 .34 show s the relative influence these strategies have on governance and m anagem ent objectives .

Figure 7 .3 3 — Exam ple 2, Step 2.1: Enterprise Strategy
Client Ser vice/Stability
Design F act or 1 Enterprise Str ategy
Impor tance of Diff erent Strategies (Input)
0
3
5
2
2
1 2 34 5

## Cost Leadership

Inno vation/Differentiation
Growth/Acquisition

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

97

# C H A P TE R  7

# E X A M P LE S

In addition to the governance and m anagem ent processes highlighted by figure 7 .34 , the follow ing other com ponents
also require attention:
Support for the portfolio m anagem ent role w ith the function responsible for overseeing all investm ents 
T he roles of enterprise architect and chief digital officer 
A  services, infrastructure and applications com ponent to facilitate autom ation and grow th, and to realize 
econom ies of scale
Influence of culture and behavior com ponent on innovation 
Figure 7 .3 4— Exam ple 2, Step 2.1: R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 1 Enterprise Strategy

Design F act or 1 Enterprise Str ategy
Resulting Go vernance/Management Objectives Importance (Output)
100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

98
Step 2 .2 : C onsider enterprise goals and apply the C OB IT  goals cascade — A t this point, the C OB IT  goals cascade can
be applied to determ ine w hich governance and m anagem ent objectives are relevant to achieve the priority enterprise
goals, based on the ranking assigned in step 1.2  ( figure 7 .35 ). Figure 7 .36 show s the relative influence these ranked
enterprise goals have on governance and m anagem ent objectives.

Figure 7 .3 5— Exam ple 2, Step 2.2: Enterprise G oals
EG01— P ortfolio of competitive products and services
EG0 2— Mana ged business risk
EG03— Compliance with external laws and r egulations
EG04— Quality of financial information
EG05— Cust omer-oriented ser vice cultur e
EG0 6— Busi ness-service continuity and availability
EG07— Quality of management information
EG08— Optimization of internal business pr ocess functionality
EG09— Optimization of business pr ocess costs
EG10— Staff skills, motiv ation and pr oductivity
EG11— Compliance with internal policies
EG12— Managed digital tr ansformation pr ogr ams
EG13— Pr oduct and business inno vation

## Design F act or 2 Enterprise Goals

5
5
2
2
2
2
2
2
4
4
3
3
3

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

99

# C H A P TE R  7

# E X A M P LE S

Figure 7 .3 6 — Exam ple 2, Step 2.2: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 2 Enterprise G oals

## Design F act or 2 Enterprise Goals

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

100
Step 2 .3 : C onsider the risk profile of the enterprise — In step 1.3 , the IT  risk categories w ere identified and analyzed
at a high level ( figure 7 .37 ). B ased on the m apping betw een the risk profile and the C OB IT  governance and
m anagem ent objectives (as explained in Section 4.2 .3 , and per the m apping table included in A ppendix D ),
figure 7 .38 show s the relative ranking of the governance and m anagem ent objectives, based on the results of the risk
analysis.

Figure 7 .3 7 — Exam ple 2, Step 2.3 : R isk P rofile

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

101

# C H A P TE R  7

# E X A M P LE S

Figure 7 .3 8— Exam ple 2, Step 2.3 : R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 3  R isk P rofile
Design F act or 3 Risk Pr ofile

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

102
Step 2 .4: C onsider current I&T -related issues — In this step, the issues identified in step 1.4 are related to the C OB IT
governance and m anagem ent objectives through a m apping table ( A ppendix E ) that associates each issue to one or
m ore governance or m anagem ent objectives that can influence that issue. B ased on the m apping (as explained in
Section 4.2 .4), figure 7 .40 show s the relative ranking of the governance and m anagem ent objectives, based on the
analysis of current I&T -related issues ( figure 7 .39) .

Figure 7 .3 9 — Exam ple 2, Step 2.4: I&T- R elated Issues

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

103

# C H A P TE R  7

# E X A M P LE S

Figure 7 .40— Exam ple 2, Step 2.4: R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 4 I& T-R elated Issues

Design F act or 4 I&T -Related Issues

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

104
Step 2 .5: Initial scope of the governance system — A t this point, it is possible to com bine the resulting governance
and m anagem ent priorities from  the previous steps to produce initial priorities for governance and m anagem ent
objectives in the governance system (figure 7 .41) .

T he follow ing m anagem ent objectives are likely to be im portant for the governance system  of this enterprise
(top five):
A PO04 M anaged innovation 
B A I08 M anaged know ledge 
A PO03  M anaged enterprise architecture 
B A I10 M anaged configuration 
B A I06 M anaged IT changes 
Figure 7 .41— Exam ple 2, Step 2.5: Initial Design Sum m ary of G overnance and M anagem ent
O bjectives Im portance
-15
-15
-25
-25
-10
-5
-10
-5
-5
-10
-10
-10
-10
-15
-30
-10
-15
10
30
50
25
25
25
30
100
50
10
10
40
15
45
10
25
20
10
-32
Step 2 Initial Design (Summar y)

## Governance and Management Objectives Importance

-100 -50

# EDM01

# EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO03

# APO04

# APO05

# APO06

# APO07

# APO08

# APO02

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01

# BAI02

# BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

0
0
0
0
0

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO09

0 50 100

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

105

# C H A P TE R  7

# E X A M P LE S

T he follow ing m anagem ent objectives seem  (for now ) the least im portant:
M E A 03  M anaged com pliance w ith external requirem ents 
E D M 05 Ensured stakeholder engagem ent 
A PO06 M anaged budget and cost 
E D M 01 Ensured governance fram ew ork setting and m aintenance 
E D M 03  Ensured risk optim ization 
D SS05 M anaged security services 
T he next step w ill determ ine w hich refinem ents are required to this initial scope of the governance system .
7.3.3  Step 3: R eﬁne the Scope of the G overnance System
In step 3 , refinem ents to the initial scope are identified, based on the rem aining set of design factors to be analyzed.
(N ot all design factors are necessarily applicable to each enterprise, and therefore, som e m ay be ignored.)  Figure
7 .42 sum m arizes the design factors 5 through 11 that are applicable to the m edium -sized innovation com pany in this
exam ple. W hen m ore than one value w as applicable for a certain design factor, it is so indicated in the value colum n
of the figure.

11
3 8 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the inform ation
security focus area content w as in developm ent and not yet released.
Figure 7 .42— G overnance System  Scope R efinem ent Table A pplied to Exam ple 2

## Ref Design Factor Value G overnance and M anagem ent

O bjectives Priority C om ponents Focus A rea
G uidance

## DF5 Threat Landscape

High 50%
Important governance and
management objectives include:

# EDM01, EDM03 

# APO01, APO03,  APO10, APO12,

# APO13, APO14

# BAI06, BAI10 

# DSS02, DSS04, DSS05, DSS06 

# MEA01, MEA03, MEA04 

Important organizational
structures include:
Security strategy 
committee

# CISO 

Important culture and
behavior aspects include:
Security awareness 
Information ﬂows:
Security policy 
Security strategy 
Information security
focus area 38
11
Normal 50%  As per the initial scope deﬁnition   N /A  COBIT core model
DF6 C om pliance Requirem ents
Normal 100%
Important management objectives
include:

# EDM01, EDM03 

# APO12 

# MEA03, MEA04 

N /A  COBIT core model

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

106
F or each design factor in figure 7 .42 , the current assessed situation can be com bined w ith the m apped governance
and m anagem ent objectives and other guidance in figure 7 .42 . T he follow ing exam ples w ere produced using m atrix
calculations betw een the input values and a m apping betw een these values and governance and m anagem ent
objectives. M apping tables are included in A ppendices F  through K  of this publication. T he resulting spider charts,
w ith the prioritized governance and m anagem ent objectives, represent relative im portance levels com pared to a
baseline level. R elative im portance levels are expressed on a scale from  -100 to +100, w ith zero (0) indicating that
there is no im pact on the im portance of a governance or m anagem ent objective, and +100 indicating that the
objective has becom e tw ice as im portant due to the design factor at hand.
12
3 9 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the digital
transform ation focus area content w as being contem plated as a potential future focus area.
13
40 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the cloud focus area
content w as being contem plated as a potential future focus area.
14
41 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the D evOps focus
area content w as in developm ent and not yet released.
Figure 7 .42— G overnance System  Scope R efinem ent Table A pplied to Exam ple 2 (cont.)

## Ref Design Factor Value G overnance and M anagem ent

O bjectives Priority C om ponents Focus A rea
G uidance
DF7 R o le o f IT
Strategic
5 on a
scale
of 5

## Combination of strategic and

factory mode (bimodal approach);
see ﬁgure 4.5 for governance and
management objectives linked to
factory and turnaround IT
Typical bimodal components,
including:
Organizational structures 
Chief digital oﬃcer 
Skills and competencies 
Staff who can work in an 
ambidextrous
environment that
combines both
exploration and
exploitation
Processes 
A portfolio and 
innovation process that
integrates exploration
and exploitation of digital
transformation
opportunities
Digital
transformation focus
area 39
12

## DF8 Sourcing M odel for IT

Cloud 100%
Important management objectives
include:

# APO09, APO10 

# MEA01 

N /A  Cloud focus area 40
13
DF9 IT Im plem entation M ethods
DevOps
Agile
Traditional
70%
15%
15%
Important governance and
management objectives include:

# BAI02, BAI03, BAI06 

Important and speciﬁc roles

## as identiﬁed in the DevOps

focus area guidance
DevOps focus area 41
14

## DF10 Technology A doption Strategy

First Mover 100%
Important governance and
management objectives include:

# EDM01, EDM02 

# APO02, APO04, APO05, APO08 

# BAI01, BAI02, BAI03, BAI05,

# BAI07, BAI11

# MEA01 

Processes that can run at a
higher pace
DevOps focus area 41
Digital
transformation focus
area

## DF11 Enterprise Size

Medium  As per the initial scope deﬁnition   N /A  SME Focus area

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

107

# C H A P TE R  7

# E X A M P LE S

Step 3 .1: C onsider the current IT  threat landscape — Figure 7 .43 depicts the threat landscape under w hich the
enterprise believes it operates. Figure 7 .44 show s the im pact on governance and m anagem ent objectives of the
assessed threat landscape.

Figure 7 .43 — Exam ple 2, Step 3 .1: Threat Landscape
Figure 7 .44— Exam ple 2, Step 3 .1: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 5 T hreat Landscape
Design F act or 5 Thr eat Landscape
50%  50%

## Normal High

Design F act or 5 Thr eat Landscape

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

108
T his classification of the threat landscape elevates the im portance of a substantial num ber of governance and
m anagem ent objectives, per the entry in figure 7 .42 related to high threat landscape. G uidance on these governance
and m anagem ent objectives m ust be draw n from  the inform ation security focus area guidance, w hich contains m ore
detailed and specific guidance on cybersecurity than does the C OB IT  core m odel. 42
15
In addition, the enterprise m ust consider the follow ing for inclusion in its governance system  design:
Im portant organizational structures, including: 
Security strategy com m ittee 

# C ISO 

Im portant culture and behavior aspects, including: 
Security aw areness 
Inform ation flow s: 
Security policy 
Security strategy 
15
42 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the inform ation
security focus area content w as in developm ent and not yet released.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

109

# C H A P TE R  7

# E X A M P LE S

Step 3 .2 : C onsider com pliance requirem ents — Figure 7 .45 depicts the com pliance requirem ents for the enterprise,
w hich are estim ated to be norm al. Figure 7 .46 show s the im pact of the assessed com pliance requirem ents on the
governance and m anagem ent objectives. T here is no im pact, w hich is the expected result, since norm al is the
baseline situation.

Figure 7 .45— Exam ple 2, Step 3 .2: C om pliance R equirem ents
Figure 7 .46 — Exam ple 2, Step 3 .2: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 6  C om pliance R equirem ents
Design F act or 6 Compliance Requir ements
100%

## Normal Low High

Design F act or 6 Compliance Requir ements

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

110
Step 3 .3 : C onsider the role of IT — Figure 7 .47 show s the role of IT , w hich is expressed as strategic. Figure 7 .48
show s the im pact of the assessed role of IT  on the governance and m anagem ent objectives.

Figure 7 .47 — Exam ple 2, Step 3 .3 : R ole of IT
Suppor t

## Design F act or 7 Role of I T

10
1
1
1
5
2 3 45
Factory
Turnaround
Str ategic
Figure 7 .48— Exam ple 2, Step 3 .3 : R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 7  R ole of IT

## Design F act or 7  Role of I T

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

111

# C H A P TE R  7

# E X A M P LE S

T he enterprise m ust also consider the follow ing typical bim odal com ponents for inclusion in its governance system
design:
Organizational structures: chief digital officer 
Skills and com petencies: staff w ho can w ork in an am bidextrous environm ent that com bines both exploration and 
exploitation
Processes: a portfolio and innovation process that integrates exploration and exploitation of digital transform ation 
opportunities
In addition to the prioritized governance and m anagem ent objectives, guidance should be draw n from  the digital
transform ation focus area (w hen available).

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

112
Step 3 .4: C onsider the sourcing m odel for IT — Figure 7 .49 depicts the selected sourcing m odel of the enterprise,
w hich is going fully cloud. Figure 7 .50 show s the im pact of the assessed sourcing m odel on the governance and
m anagem ent objectives. T he diagram  show s that this im pact is focused on three m anagem ent objectives only. In
addition, the enterprise w ill have to draw  upon the cloud focus area guidance (w hen available).

Figure 7 .49 — Exam ple 2, Step 3 .4: Sourcing M odel for IT

## Design F act or 8 Sour cing Model for I T

100%
Cloud Insour cing Outsour cing
Figure 7 .50— Exam ple 2, Step 3 .4: R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 8 Sourcing M odel for IT

## Design F act or 8 Sour cing Model for I T

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

113

# C H A P TE R  7

# E X A M P LE S

Step 3 .5: C onsider IT  im plem entation m ethods — T he enterprise is using a m ostly D evOps IT  im plem entation m ethod
(see figure 7.51 ). Figure 7.52 show s the im pact this has on governance and m anagem ent objectives. G uidance
should be draw n from  the D evOps m anagem ent focus area, as indicated in figure 7 .42 .

Figure 7 .51— Exam ple 2, Step 3 .5: IT Im plem entation M ethods
Figure 7 .52— Exam ple 2, Step 3 .5: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 9  IT Im plem entation M ethods

## Design F act or 9 IT Implementation Methods

## Resulting Go vernance/Management Objectives Importance

200
100
125
150
175
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

55-75 75 5-7 5
00 000 00 -10 10 0
-50 50 50
-25 225
000

## Design F act or 9  IT Implementation Methods

## DevOps TraditionalAgile

70%
15%
15%

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

114
Step 3 .6: C onsider the  technology adoption strategy — Figure 7 .53 indicates that the enterprise is a first m over w hen
it com es to adopting new  technology. Figure 7 .54 show s the im pact this has on the governance and m anagem ent
objectives priorities.

In addition to the prioritized governance and m anagem ent objectives, guidance should be draw n from  the digital
transform ation and D evOps focus areas (w hen available).
Figure 7 .53 — Exam ple 2, Step 3 .6 : Technology A doption Strategy
Figure 7 .54— Exam ple 2, Step 3 .6 : R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 10 Technology A doption Strategy

## Design F act or 10 Technology Adoption Strategy

100%

## Follower Slow Adopter First Mo ver

## Design F act or 10 Technology Adoption Strategy

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

115

# C H A P TE R  7

# E X A M P LE S

Step 3 .7: C onsider enterprise size — T he enterprise is m edium -sized. Per figure 7 .42 , this m eans that the sm all and
m edium  enterprise focus area 43
16 should be used as the basis for the definition of the governance system .
7.3.4  Step 4: C onclude the G overnance Solution Design
T he last step in the design process requires all inputs from  previous steps to be discussed, conflicts resolved and a
conclusion reached. T he resulting governance system  reflects careful consideration of all inputs, taking into account
that these inputs w ere som etim es conflicting, and choices had to be m ade.
7.3.4.1  G overnance and M anagem ent O bjectives
A t this point, it is possible to add the governance and m anagem ent priorities resulting from  steps 3 .1 through 3 .7 to
the results obtained from  the initial governance system  design in steps 2 .1 through 2 .4. T his synthesis results in the
follow ing adjusted priorities for governance and m anagem ent objectives in the governance system  ( figure 7 .55) .

16
43 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the sm all and m edium
enterprise focus area content w as in developm ent and not yet released.
Figure 7 .55— Exam ple 2, Step 4.1: G overnance and M anagem ent O bjectives Im portance (A ll Design Factors)

## Governance and Management Objectives Importance (All Design Factors)

-100 -50

# EDM01

# EDM02

# EDM03

# EDM04 30

55
50
35
100
45
25
45
55
90
35
55
55
55
20
85
65
25
20

# EDM05

# APO01

# APO03

# APO04

# APO05

# APO06 -10

# APO07

# APO08

# APO02

# APO10

# APO11

# APO12

# APO13

# APO14

45
10
60
30

# BAI01

# BAI02

# BAI03

# BAI04

70
10

# BAI05

# BAI06

# BAI07

65
70

# BAI08

# BAI09

# BAI10 85

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

50
35
45
30
35
30

# 30DSS06

# MEA01

# MEA02

65
15
0
15

# MEA03

# MEA04

# APO09

0 50 100

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

116
T he follow ing m anagem ent objectives are likely to be im portant for the governance system  of this enterprise:
A PO03  M anaged enterprise architecture (100) 
A PO04 M anaged innovation (9 0) 
A PO07 M anaged hum an resources (85) 
B A I10 M anaged configuration (85) 
B A I03  M anaged solutions identification and build (70) 
B A I07 M anaged IT change acceptance and transitioning (70) 
T he m ost im portant objectives have changed slightly com pared to the list identified in the initial scope definition in step 2 .5.
T he follow ing m anagem ent objectives seem  the least im portant:
A PO06 M anaged budget and cost 
M E A 03  M anaged com pliance w ith external requirem ents 
A PO11 M anaged projects 
B A I04 M anaged availability and capacity 
W hen com paring this result to the initial scope, the follow ing observations can be m ade:
Overall, m ost governance/m anagem ent objectives have gained significant im portance after taking into account the 
additional design factors; this can be explained by the high threat landscape and strategic role of I&T .
T he governance/m anagem ent objectives that ranked highest after the initial scope definition generally still rank 
high after scope refinem ent.
T he enterprise decides that it is satisfied w ith the rating of governance and m anagem ent objectives im portance.
A fter discussion, the enterprise decides that the first stage of its governance system  design w ill consist of the
governance and m anagem ent objectives (w ith the underlying processes) show n in figure 7 .56 .

Figure 7 .56 — Exam ple 2 G overnance and M anagem ent O bjectives w ith Target P rocess C apability
Levels
Reference G overnance/M anagem ent O bjective Target Process
C apability Level
EDM 01 Ensured governance framework setting and maintenance 2
EDM 02 Ensured beneﬁts delivery 3
EDM 03 Ensured risk optimization 3
EDM 04 Ensured resource optimization 2
EDM 05 Ensured stakeholder engagement 2
A PO 01 Managed I&T management framework 2
A PO 02 Managed strategy 2
A PO 03 Managed enterprise architecture 4
A PO 04 Managed innovation 4
A PO 05 Managed portfolio 3
A PO 07 Managed human resources 4
A PO 08 Managed relationships 3
A PO 09 Managed service agreements 2
A PO 10 Managed vendors 2
A PO 12 Managed risks 3
A PO 14 Managed data 2

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

117

# C H A P TE R  7

# E X A M P LE S

Figure 7 .56 show s the reference, governance or m anagem ent objective title, and the target capability level at w hich
the related processes should be im plem ented. G iven the high im portance of a num ber of processes, the target
capability level has been set at a higher value (3  or 4). T he logic applied by the enterprise is the sam e used in
E xam ple 1:
A ny governance/m anagem ent objective that scored 75 or higher— m eaning that its im portance w as at least 75% 
higher than com pared to a benchm ark situation— w ould require a capability level 4.
A ny governance/m anagem ent objective that scored 50 or higher w ould require a capability level 3 . 
A ny governance/m anagem ent objective that scored 2 5 or higher w ould require a capability level 2 . 
7.3.4.2   O ther C om ponents
T he enterprise w ill pay specific attention to a strong im plem entation of the follow ing roles and structures (along w ith
other com ponents) of the governance system :
Support for the portfolio m anagem ent role w ith an investm ent office 
R oles of enterprise architect and chief digital officer 
A  services, infrastructure and applications com ponent to facilitate autom ation and grow th, and realize econom ies 
of scale
Influence of culture and behavior com ponent for innovation 
Im portant organizational structures, including: 
Security strategy com m ittee 

# C ISO 

Im portant culture and behavior aspects, including: 
Security aw areness 
Figure 7 .56 — Exam ple 2 G overnance and M anagem ent O bjectives w ith Target P rocess C apability
Levels (cont.)
Reference G overnance/M anagem ent O bjective Target Process
C apability Level
BA I01 Managed programs 2
BA I02 Managed requirements deﬁnition 3
BA I03 Managed solutions identiﬁcation and build 3
BA I05 Managed organizational change 3
BA I06 Managed IT changes 3
BA I07 Managed IT change acceptance and transitioning 3
BA I08 Managed knowledge 3
BA I10 Managed conﬁguration 4
BA I11 Managed projects 2
DSS01 Managed operations 3
DSS02 Managed service requests and incidents 2
DSS03 Managed problems 2
DSS04 Managed continuity 2
DSS05 Managed security services 2
DSS06 Managed business process controls 2
M EA 01 Managed performance and conformance monitoring 3

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

118
Inform ation flow s: 
Security policy 
Security strategy 
Skills and com petencies: staff w ho can w ork in an am bidextrous environm ent that com bines both exploration and 
exploitation
Processes: a portfolio and innovation process that integrates exploration and exploitation of digital transform ation 
opportunities
7.3.4.3  S pecific Focus A rea G uidance
T he enterprise w ill use the follow ing guidance to com plem ent the core C OB IT  guidance:
T he sm all and m edium  enterprise focus area guidance, because it is tailored for use by sm aller organizations 
Inform ation security focus area guidance, given the high threat landscape, and the results of the risk analysis and 
the current I&T -related issues
D evOps, cloud and digital transform ation focus area guidance, w hen and w here applicable and available 
7.4  E xam ple 3: H igh-P roﬁle G overnm ent A gency
T his case study show s the application of the w orkflow  to design a tailored governance system  for a high-profile,
large governm ent agency that provides healthcare, financial paym ents, education and other services to constituents
needing assistance. Its operations are decentralized, w ith hospitals, clinics and offices in regions nationw ide. Its I&T
budget and planning and operations budget are spread am ong hospitals, financial benefits and other business units,
w ith the IT  shop providing infrastructure support, netw ork operations and a security operations center. T he agency
considers I&T  as critical to the success of the organization, and it m ust com ply w ith law s and regulations, especially
healthcare regulations that continue to em erge. It applies a traditional approach to new  developm ent and operations,
and is hesitant to adopt new  technologies. T here is a very active audit function and dozens of significant findings
exist related to how  the agency protects its I&T , especially w ith respect to security and privacy. A s a governm ent
agency, it is a m ajor target of hackers and has just experienced a m ajor hack of its entire beneficiary file.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

119

# C H A P TE R  7

# E X A M P LE S

7.4.1  Step 1: U nderstand the E nterprise C ontext and Strategy
T he first step is to sum m arize the external and internal context of the agency.
Step 1.1: U nderstand enterprise strategy — T he agency’s focus on providing outstanding services to constituents is
reflected in figure 7 .57 .

Figure 7 .57 — Exam ple 3 , Step 1.1: Enterprise Strategy
Client Ser vice/Stability
Design F act or 1 Enterprise Str ategy
Impor tance of Diff erent Strategies (Input)
1
1
1
3
5
0 2 34 5

## Cost Leadership

Inno vation/Differentiation
Growth/Acquisition

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

120
Step 1.2 : U nderstand enterprise goals — T he agency has ranked the 13  generic enterprise goals on a scale from  1 to 5,
as depicted in figure 7 .58 . T he diagram  show s that E G 02  M anaged business risk, E G 03  C om pliance w ith external
law s and regulations, E G 05 C ustom er-oriented service culture and E G 09  O ptim ization of business process costs are
the highest-ranked enterprise goals.

Figure 7 .58— Exam ple 3 , Step 1.2: Enterprise G oals
EG01— P ortfolio of competitive products and services
EG0 2— Mana ged business risk
EG03— Compliance with external laws and r egulations
EG04— Quality of financial information
EG05— Cust omer-oriented ser vice cultur e
EG0 6— Busi ness-service continuity and availability
EG07— Quality of management information
EG08— Optimization of internal business pr ocess functionality
EG09— Optimization of business pr ocess costs
EG10— Staff skills, motiv ation and pr oductivity
EG11— Compliance with internal policies
EG12— Managed digital tr ansformation pr ogr ams
EG13— Pr oduct and business inno vation

## Design F act or 2 Enterprise Goals

5
5
5
5
2
2
2
2
1
1
4
3
3

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

121

# C H A P TE R  7

# E X A M P LE S

Step 1.3 : U nderstand the risk profile — A  high-level risk analysis resulted in the risk profile show n in figure 7 .59 .

Figure 7 .59 — Exam ple 3 , Step 1.3 : R isk P rofile

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

122
Step 1.4: U nderstand current I&T -related issues — A n analysis of the current situation resulted in the assessm ent of
current I&T -related issues show n in figure 7 .60 .

Figure 7 .6 0— Exam ple 3 , Step 1.4: I&T- R elated Issues

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

123

# C H A P TE R  7

# E X A M P LE S

7.4.2   Step 2 : Determ ine the Initial Scope of the G overnance System
T he initial scope of the governance system  is determ ined by using the inform ation (partial or in full) collected during
step 1. Step 2  translates this inform ation on enterprise strategy, enterprise goals, risk profile and I&T -related issues
into relevant governance com ponents.
Step 2 .1: C onsider enterprise strategy — T he follow ing diagram  represents the enterprise strategy, as identified in step 1.1
(figure 7 .61 ). Figure 7 .62 show s the relative influence these strategies have on governance and m anagem ent objectives .

Figure 7 .6 1— Exam ple 3 , Step 2.1: Enterprise Strategy
Figure 7 .6 2— Exam ple 3 , Step 2.1: R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 1 Enterprise Strategy

Client Ser vice/Stability
Design F act or 1 Enterprise Str ategy
10
1
1
3
5
2 3 45

## Cost Leadership

Inno vation/Differentiation
Growth/Acquisition
Design F act or 1 Enterprise Str ategy
Resulting Go vernance/Management Objectives Importance (Output)
100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

124
Step 2 .2 : C onsider enterprise goals and apply the C OB IT  goals cascade — A t this point, the C OB IT  goals cascade is
applied to determ ine w hich governance and m anagem ent objectives are relevant to achieve the priority enterprise
goals, based on their ranking assigned in step 1.2  ( figure 7 .63 ). Figure 7 .64 show s the relative influence these
ranked enterprise goals have on governance and m anagem ent objectives.

Figure 7 .6 3 — Exam ple 3 , Step 2.2: Enterprise G oals
EG01— P ortfolio of competitive products and services
EG0 2— Mana ged business risk
EG03— Compliance with external laws and r egulations
EG04— Quality of financial information
EG05— Cust omer-oriented ser vice cultur e
EG0 6— Busi ness-service continuity and availability
EG07— Quality of management information
EG08— Optimization of internal business pr ocess functionality
EG09— Optimization of business pr ocess costs
EG10— Staff skills, motiv ation and pr oductivity
EG11— Compliance with internal policies
EG12— Managed digital tr ansformation pr ogr ams
EG13— Pr oduct and business inno vation

## Design F act or 2 Enterprise Goals

5
5
5
5
2
2
2
2
1
1
4
3
3

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

125

# C H A P TE R  7

# E X A M P LE S

Figure 7 .6 4— Exam ple 3 , Step 2.2: R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 2 Enterprise G oals

## Design F act or 2 Enterprise Goals

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

126
Step 2 .3 : C onsider the risk profile of the enterprise — In step 1.3 , IT  risk categories w ere identified and analyzed at a
high level ( figure 7 .65 ). B ased on the m apping betw een the risk profile and the C OB IT  governance and m anagem ent
objectives (as explained in Section 4.2 .3 , and per the m apping table included in A ppendix D ), figure 7 .66 show s the
relative ranking of the governance and m anagem ent objectives based on the results of the risk analysis.

Figure 7 .6 5— Exam ple 3 , Step 2.3 : R isk P rofile

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

127

# C H A P TE R  7

# E X A M P LE S

Figure 7 .6 6 — Exam ple 3 , Step 2.3 : R esulting G overnance/M anagem ent O bjectives Im portance for
Design Factor 3  R isk P rofile
Design F act or 3 Risk Pr ofile

## Resulting Go vernance/Management Objectives Importance

100
75
50
25
-75
-100
-50
-25
0

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

128
Step 2 .4: C onsider current I&T -related issues — In this step, the issues identified in step 1.4 are related to the C OB IT
governance and m anagem ent objectives through a m apping table ( A ppendix E ) that associates each issue to one or
m ore governance or m anagem ent objectives that can influence that issue ( figure 7 .67 ). B ased on the m apping (as
explained in Section 4.2 .4), Figure 7 .68 show s the relative ranking of the governance and m anagem ent objectives,
based on the analysis of current I&T -related issues.

Figure 7 .6 7 — Exam ple 3 , Step 2.4: I&T- R elated Issues

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

129

# C H A P TE R  7

# E X A M P LE S

Figure 7 .6 8— Exam ple 3 , Step 2.4: R esulting G overnance/M anagem ent O bjectives Im portance for

## Design Factor 4 I& T-R elated Issues

# EDM01 EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO02

# APO03

# APO04

# APO05

# APO06

# APO09

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01 BAI02 BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO07

# APO08

100
75
50
25
-75
-100
-50
-25
0
Design F act or 4 I&T -Related Issues

## Resulting Go vernance/Management Objectives Importance

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

130
Step 2 .5: Initial scope of the governance system — A t this point, it is possible to com bine the resulting governance
and m anagem ent priorities from  the previous steps. T he initial results w ere discussed w ith m anagem ent, and adjusted
for tw o m anagem ent objectives: A PO02  M anaged strategy (w hose priority increased) and A PO09  M anaged service
agreem ents (w hose priority decreased). T hese adjustm ents resulted in the follow ing initial priorities for governance
and m anagem ent objectives in the governance system .

T he follow ing governance and m anagem ent objectives are likely to be im portant for the governance system  of this
agency, considering all governance and m anagem ent objectives w ith a priority rating equal to or higher than 60:
A PO13  M anaged security (100) 
A PO12  M anaged risk (80) 
D SS02  M anaged service requests and incidents (75) 
B A I04 M anaged availability and capacity (75) 
B A I09  M anaged assets (60) 
Figure 7 .6 9 — Exam ple 3 , Step 2.5: Initial Design Sum m ary of G overnance and M anagem ent
O bjectives Im portance
Step 2 Initial Design (Summar y)

## Governance and Management Objectives Importance

-100 -50

# EDM01

# EDM02

# EDM03

# EDM04

55
25
25
20
10
15
25

# EDM05

# APO01

-40
-20

# APO03 -35

# APO04 -40

# APO05

# APO06 -10

-25

# APO07 -25

-15

# APO08

# APO02

# APO10

# APO11

# APO12

# APO13

# APO14

50
80
100
30
5
0
5
75

# -10 BAI01

# BAI02

# BAI03

# BAI04

# BAI05

# BAI06

# BAI07

25
10

# -40 BAI08

# BAI09

# BAI10

60
25

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

15
20
75
50
55
25
55

# DSS06

# MEA01

# MEA02

5
35
20

# MEA03

# MEA04 25

# APO09

0 50 100

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

131

# C H A P TE R  7

# E X A M P LE S

T he follow ing m anagem ent objectives seem  (for now ) the least im portant (scoring less than -2 5):
A PO02  M anaged strategy 
A PO04 M anaged innovation 
B A I08 M anaged know ledge 
A PO03  M anaged enterprise architecture 
T he next step w ill determ ine w hich refinem ents are required to this initial scope of the governance system .
7.4.3   Step 3: R eﬁne the Scope of the G overnance System
In step 3 , refinem ents to the initial scope are identified, based on the set of design factors included to be analyzed. N ot all
design factors m ight be applicable for each enterprise, in w hich case they can be ignored. Figure 6.7 0 show s a sum m ary of
the design factors 5 through 11 that are applicable to the m id-sized innovation com pany in this exam ple.W hen m ore than
one value w as applicable for a certain design factor, it is so indicated in the value colum n of the figure.

17
44 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the Inform ation
security focus area content w as in developm ent and not yet released.
Figure 7 .7 0— G overnance System  Scope R efinem ent Table A pplied to Exam ple 3

## Ref Design

Factor Value G overnance and M anagem ent
O bjectives Priority C om ponents Focus A rea
G uidance

## DF5 Threat Landscape

High 100%
Important governance and
management objectives include:

# EDM01, EDM03 

# APO01, APO03,  APO10, APO12,

# APO13, APO14

# BAI06, BAI10 

# DSS02, DSS04, DSS05, DSS06 

# MEA01, MEA03, MEA04 

Important organizational
structures include:
Security strategy 
committee

# CISO 

Important culture and
behavior aspects include:
Security awareness 
Information ﬂows:
Security policy 
Security strategy 
Information security
focus area 44
17
DF6 C om pliance Requirem ents
Low 100%  As per the initial scope deﬁnition   N /A  COBIT core model

## DF7 Role of IT

## Support 5 on a

scale of 5
As per the initial scope deﬁnition   N /A  COBIT core model

## DF8 Sourcing M odel for IT

Insourced 100%  As per the initial scope deﬁnition   N /A  COBIT core model
DF9 IT Im plem entation M ethods
Traditional 100%  As per the initial scope deﬁnition   N /A  COBIT core model

## DF10 Technology A doption Strategy

Follower 100%
Important governance and
management objectives include:

# APO02, APO04 

# BAI01 

Processes that can run at a
slower pace
COBIT core model

## DF11 Enterprise Size

Large  As per the initial scope deﬁnition   N /A  COBIT core model

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

132
In both previous exam ples, the application of each D esign F actor w as fully detailed. T his exam ple does not include
the detailed calculations and diagram s and presents only the end result. In addition to applying the design factors as
explained in figure 7 .7 0 , the im portance of aligning processes w ith their I&T  strategy is stressed again.
7.4.4  Step 4: C onclude the G overnance Solution Design
T he last step in the design process requires all inputs from  previous steps to be discussed, conflicts resolved and a
conclusion reached. T he resulting governance system  is the result of careful consideration of all inputs, taking into
account that these inputs w ere som etim es conflicting and choices had to be m ade, including the discussion raising
the im portance of the A PO02  M anaged strategy objective.
7.4.4.1  G overnance and M anagem ent O bjectives
A t this point, it is possible to com bine the resulting governance and m anagem ent priorities from  steps 3 .1 through
3 .7 to the results obtained from  the initial governance system  design in steps 2 .1 through 2 .4. T his results in the
follow ing adjusted priorities for governance and m anagem ent objectives in the governance system .

Figure 7 .7 1— Exam ple 3 , Step 4: G overnance and M anagem ent O bjectives Im portance (A ll Design Factors)
-100 -50 05 0 100
-30
-40
-25
-10
-10
-20
-25
-20
-10
-5
-10
-30
100
30
5
5
0
0
0
0
0
20
25
25
50
40
100
35
60
35
40
30
70
35
65
30
65
55
10
35
30

## Governance and Management Objectives Importance (All Design Factors)

# EDM01

# EDM02

# EDM03

# EDM04

# EDM05

# APO01

# APO03

# APO04

# APO05

# APO06

# APO07

# APO08

# APO02

# APO10

# APO11

# APO12

# APO13

# APO14

# BAI01

# BAI02

# BAI03

# BAI04

# BAI05

# BAI06

# BAI07

# BAI08

# BAI09

# BAI10

# BAI11

# DSS01

# DSS02

# DSS03

# DSS04

# DSS05

# DSS06

# MEA01

# MEA02

# MEA03

# MEA04

# APO09

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

133

# C H A P TE R  7

# E X A M P LE S

T he follow ing governance and m anagem ent objectives are likely to be im portant for the governance system  of this
agency, considering all governance and m anagem ent objectives w ith a priority rating equal to or higher than 60:
A PO13  M anaged security (100) 
D SS02  M anaged service requests and incidents (70) 
D SS05 M anaged security services (65) 
D SS04 M anaged continuity (65) 
B A I04 M anaged availability and capacity (60) 
T he follow ing m anagem ent objectives seem  the least im portant (scoring less than -50):
A PO04 M anaged innovation (-40) 
A PO02  M anaged strategy (-3 0) 
B A I08 M anage know ledge (-3 0) 
A PO05 M anaged portfolio (-2 5) 
B A I03  M anaged solutions identification and build (-2 5) 
T he final result reflects several changes relative to priorities in the initial design (obtained after Step 2 ).
A fter discussion, the agency decided that its governance system  design w ill consist of the prioritized list of
governance and m anagem ent objectives (w ith the underlying processes) show n in figure 7 .7 2 . T he figure contains all
the C OB IT  governance and m anagem ent objectives, the suggested capability level based on the outcom e of Step 3 ,
and the actual decision m anagem ent has taken about target capability levels.

Figure 7 .7 2— Exam ple 3  G overnance and M anagem ent O bjectives and Target P rocess C apability
Levels
Reference G overnance/M anagem ent O bjective
Suggested

## Target Process

C apability Level

## Decided Target

Process
C apability Level
EDM 01 Ensured governance framework setting and maintenance 1 3
EDM 02 Ensured beneﬁts delivery 1 3
EDM 03 Ensured risk optimization 2 3
EDM 04 Ensured resource optimization 1 3
EDM 05 Ensured stakeholder engagement 2 3
A PO 01 Managed IT management framework 2 2
A PO 02 Managed strategy 1 3
A PO 03 Managed enterprise architecture 1 2
A PO 04 Managed innovation 1 1
A PO 05 Managed portfolio 1 3
A PO 06 Managed budget and costs 1 3
A PO 07 Managed human resources 1 2
A PO 08 Managed relationships 1 2
A PO 09 Managed service agreements 1 2
A PO 10 Managed vendors 1 2
A PO 11 Managed quality 3 3
A PO 12 Managed risk 2 4
A PO 13 Managed security 4 4
A PO 14 Managed data 3 4
BA I01 Managed programs 1 3

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

134
It is m anagem ent’s prerogative to define target levels that differ from  the ones suggested by a (sem i)autom ated
approach, because m apping tables and generic goals and conditions m ay not alw ays be suited to the enterprise’s
particular context. In figure 7 .7 2 , the suggested target capability level and the decided target level w ere identical— or
varied by only one level— in alm ost 80 percent of the governance and m anagem ent objectives.
T he greatest deviations occurred in governance and m anagem ent objectives related to cost and budgeting of IT ,
program s and projects, and strategy. A lthough the assessm ents of enterprise strategy, enterprise goals, risk, I&T
issues and other design factors indicated low er priorities for governance and m anagem ent objectives, m anagem ent
decided to give these objectives higher targets in order to address the agency’s governance issues.
7.4.4.2    O ther C om ponents
T he agency w ill pay specific attention to a strong im plem entation of the follow ing roles and structures (along w ith
other com ponents) of the governance system :
T he agency w ill issue a top m anagem ent policy expressing strong support for establishing an I&T  governance 
structure, standards, policies and procedures, and for im plem enting the follow ing structures and roles. (T he actual
I&T  governance and organizational structures im plem ented by this high-profile large governm ent agency follow s
in figure 7 .7 3 .)
Figure 7 .7 2— Exam ple 3  G overnance and M anagem ent O bjectives and Target P rocess C apability
Levels (cont.)
Reference G overnance/M anagem ent O bjective
Suggested

## Target Process

C apability Level

## Decided Target

Process
C apability Level
BA I02 Managed requirements deﬁnition 1 2
BA I03 Managed solutions identiﬁcation and build 1 2
BA I04 Managed availability and capacity 3 2
BA I05 Managed organizational change 1 2
BA I06 Managed IT changes 2 2
BA I07 Managed IT change acceptance and transitioning 1 2
BA I08 Managed knowledge 1 1
BA I09 Managed assets 2 2
BA I10 Managed conﬁguration 2 2
BA I11 Managed projects 1 3
DSS01 Managed operations 1 2
DSS02 Managed service requests and incidents 3 2
DSS03 Managed problems 2 2
DSS04 Managed continuity 3 2
DSS05 Managed security services 3 3
DSS06 Managed business process controls 2 3
M EA 01 Managed performance and conformance monitoring 1 2
M EA 02 Managed system of internal control 2 2
M EA 03 Managed compliance with external requirements 2 2
M EA 04 Managed assurance 2 2

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

135

# C H A P TE R  7

# E X A M P LE S

In term s of organizational structures, it w as decided to im plem ent the follow ing roles: 
Strategic m anagem ent council 
IT  leadership board 
B udgeting and near-term  issues board 
Program m ing and long-term  issues board 
W orkforce planning process 
C apital asset planning and investm ent process 
Legislative developm ent process 

T he agency w ill also ensure adequate risk, security and privacy aw areness throughout the organization.
7.4.4.3  S pecific Focus A rea G uidance
T he agency w ill use the follow ing guidance to com plem ent the core C OB IT  guidance: 45
18
R isk focus area content, given the high threat landscape, and the results of the risk analysis and current I&T  issues 
Inform ation security focus area guidance, given the high threat landscape, and the results of the risk analysis and 
the current I&T  issues
18
45 A t the tim e of publication of the C O BIT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution , the risk and
inform ation security focus areas are in developm ent and not yet released.
Figure 7 .7 3 — Exam ple 3 , Step 4: O rganizational Structures
Budget F ormulation
Str ategic Management Council (SMC )

## Executive Board

Budget
Formulation
Process
Workforce
Planning
Process

## Capital Asset

## Planning and

Inv estment
Process
Legislativ e
Development
Process
Field
Governance
Program/Initiative
Boar ds
(e.g., HeV , FLI TE)
Specializ ed
Boar ds

## (e.g., SL A’s Data

Management)
Programming

## and Long Term

Issues Boar d

# (PL TI)

Information
Technology
Leadership
Boar d (I TLB)
Budgeting

## and Near Term

Issues Boar d

# (BN TI)

Business
Relationships
Meetings
(Admins and

## Staff Office)

Str ategic
Planning
and P olicy
Formulation
Process
Budget F ormulation
Budget F ormulation

## and Other Issues

Budget F ormulation

## and Other Issues

## Organizational Structures

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

136
P age intentionally left blank

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

137

# A P P E N DIC E S

# A P P E N DIX  A

# A P P E N DIC E S

T he follow ing appendices contain the m apping tables betw een the governance and m anagem ent objectives and the
design factors that w ere identified in Section 2 .6.
T he m appings express the degree to w hich design factor values influence the im portance of a governance or
m anagem ent objective.
T he m appings use a scale from  zero (0) to four  (4): 4 indicates the m ost influence, and 0 indicates the absence of
any relationship.
E xam ple : W hen an enterprise selects grow th strategy for D F 2  Enterprise strategy , the A ppendix A  m apping
show s that m anagem ent objective A PO03  M anaged enterprise architecture w ill be very im portant (a value of 4).
Appendix A : M apping T able— E nterprise Strategies to G overnance and M anagem ent
O bjectives

Figure A .1— M apping Enterprise Strategies to G overnance and M anagem ent O bjectives
DF1 G row th/A cquisition Innovation/Differentiation C ost Leadership C lientService/Stability

# EDM 01 1.0 1.0 1.5 1.5

# EDM 02 1.5 1.0 2.0 3 .5

# EDM 03 1.0 1.0 1.0 2.0

# EDM 04 1.5 1.0 4.0 1.0

# EDM 05 1.5 1.5 1.0 2.0

# A PO 01 1.0 1.0 1.0 1.0

# A PO 02 3 .5 3 .5 1.5 1.0

# A PO 03 4.0 2.0 1.0 1.0

# A PO 04 1.0 4.0 1.0 1.0

# A PO 05 3 .5 4.0 2.5 1.0

# A PO 06 1.5 1.0 4.0 1.0

# A PO 07 2.0 1.0 1.0 1.0

# A PO 08 1.0 1.5 1.0 3 .5

# A PO 09 1.0 1.0 1.5 4.0

# A PO 10 1.0 1.0 3 .5 1.5

# A PO 11 1.0 1.0 1.0 4.0

# A PO 12 1.0 1.5 1.0 2.5

# A PO 13 1.0 1.0 1.0 2.5

# A PO 14 1.0 1.0 1.0 1.0

# BA I01 4.0 2.0 1.5 1.5

# BA I02 1.0 1.0 1.5 1.0

# BA I03 1.0 1.0 1.5 1.0

# BA I04 1.0 1.0 1.0 3 .0

# BA I05 4.0 2.0 1.0 1.5

# BA I06 2.0 2.0 1.0 1.5

# BA I07 1.5 2.0 1.0 1.5

# BA I08 1.0 3 .5 1.0 1.0

# BA I09 1.0 1.0 1.0 1.0

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

138
Figure A .1— M apping Enterprise Strategies to G overnance and M anagem ent O bjectives (cont.)
DF1 G row th/A cquisition Innovation/Differentiation C ost Leadership C lientService/Stability

# BA I10 1.0 1.0 1.0 1.0

# BA I11 3 .5 3 .0 1.5 1.0

# DSS01 1.0 1.0 1.0 1.5

# DSS02 1.0 1.0 1.0 4.0

# DSS03 1.0 1.0 1.0 3 .0

# DSS04 1.0 1.0 1.0 4.0

# DSS05 1.0 1.0 1.0 2.5

# DSS06 1.0 1.0 1.0 1.5

# M EA 01 1.0 1.0 1.0 1.0

# M EA 02 1.0 1.0 1.0 1.0

# M EA 03 1.0 1.0 1.0 1.0

# M EA 04 1.0 1.0 1.0 1.0

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

139

# A P P E N DIC E S

# A P P E N DIX  B

Appendix B : M apping T able— E nterprise G oals to A lignm ent G oals

Figure A .2— M apping Enterprise G oals to A lignm ent G oals

## EG01 EG02 EG03 EG04 EG05 EG06 EG07 EG08 EG09 EG10 EG11 EG12 EG13

## Portfolio of

competitive
products
and
services
Managed
business
risk
Compliance
with external
laws and
regulations

## Quality of

financial
information
Customer-
oriented
service
culture
Business
service
continuity
and
availability

## Quality of

management
information
Optimization
of internal
business
process
functionality
Optimization
of business
process
costs
Staff skills,
motivation
and
productivity
Compliance
with internal
policies
Managed
digital
transformation
programs
Product
and
business
innovation

## AG01 I&T compliance and

support for business
compliance with external
laws and regulations

# S P S

## AG02 Managed I&T-related risk P S

AG03 Realized benefits from
I&T-enabled investments
and services portfolio

# S S S S P

## AG04 Quality of technology-

related financial
information

# P P P

## AG05 Delivery of I&T services

in line with business
requirements

# P S S S S

AG06 Agility to turn business
requirements into
operational solutions

# P S S S S

## AG07 Security of information,

processing infrastructure
and applications, and
privacy

# P P

## AG08 Enabling and supporting

business processes by
integrating applications
and technology

# P P S S P S

AG09 Delivering programs
on time, on budget and
meeting requirements and
quality standards

# P S S S P S

## AG10 Quality of I&T

management information P P S

## AG11 I&T compliance with

internal policies S P P

## AG12 Competent and

motivated staff with
mutual understanding of
technology and business

# S P

## AG13 Knowledge, expertise and

initiatives for business
innovation

# P S S P

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

140

# C O B IT ® 2 0 19 DE SIG N  G U IDE

Appendix C : M apping T able— A lignm ent G oals to G overnance and M anagem ent
O bjectives

Figure A .3 — M apping A lignm ent G oals to G overnance and M anagem ent O bjectives

## AG01 AG02 AG03 AG04 AG05 AG06 AG07 AG08 AG09 AG10 AG11 AG12 AG13

# I&T

compliance
and support
for business
compliance
with
external
laws and
regulations
Managed
I&T -related
risk
Realized
benefits from
I&T -enabled
investments
and services
portfolio

## Quality of

technology-
related
financial
information

## Delivery of

I&T services
in line with
business
requirements
Agility to turn
business
requirements
into
operational
solutions

## Security of

information,
processing
infrastructure
and
applications,
and privacy

## Enabling and

supporting
business
processes by
integrating
applications
and
technology
Delivering
programs
on time, on
budget and
meeting
requirements
and quality
standards
Quality

## of I&T

management
information

# I&T

compliance
with internal
policies

## Competent and

motivated staff
with mutual
understanding
of technology
and business
Knowledge,
expertise and
initiatives
for business
innovation
EDM01 Ensured governance
framework setting and
maintenance

# P S P S S

## EDM02 Ensured benefits delivery P S S SS

## EDM03 Ensured risk optimization S P P S

EDM04 Ensured resource

## optimization S S S S P S

EDM05 Ensured stakeholder

## engagement S P S

## APO01 Managed I&T

## management framework S S P S S SS S P

## APO02 Managed strategy S S S P SS

APO03 Managed enterprise

## architecture S S P S P

## APO04 Managed innovation S P SS P

## APO05 Managed portfolio P P SS S

## APO06 Managed budget and

## costs S P P S

APO07 Managed human

## resources S SS P P

## APO08 Managed relationships S P P SS P P

APO09 Managed service
agreements P S

## APO10 Managed vendors P SS

## APO11 Managed quality SS S P P

## APO12 Managed risk P P

## APO13 Managed security S S P

## APO14 Managed data S S S S P

## BAI01 Managed programs P SS P

BAI02 Managed requirements

## definition S P P S P S

BAI03 Managed solutions

## identification and build S P P S P

## BAI04 Managed availability and

## capacity P S S

BAI05 Managed organizational

## changes P S S P P S

## BAI06 Managed IT changes S S P S

## BAI07 Managed IT change

acceptance and
transitioning

# S P S

## BAI08 Managed knowledge SS S S P P

## BAI09 Managed assets P S

## BAI10 Managed configuration S P

## BAI11 Managed projects P S P P

## DSS01 Managed operations P S

DSS02 Managed service requests

## and incidents S P S

## DSS03 Managed problems S P S

## DSS04 Managed continuity S P P

## DSS05 Managed security services S P S P S

DSS06 Managed business
process controls SS S P S
MEA01 Managed performance
and conformance
monitoring

# SS P S P S

## MEA02 Managed system of

## internal control S SS S S S S P

## MEA03 Managed compliance with

external requirements P S

## MEA04 Managed assurance SS S S S S P

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# A P P E N DIC E S

# A P P E N DIX  D

141
Appendix D: M apping T able— IT R isk to G overnance and M anagem ent O bjectives

Figure A .4— M apping IT R isk to G overnance and M anagem ent O bjectives

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

142

Figure A .4— M apping IT R isk to G overnance and M anagem ent O bjectives (cont.)

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# A P P E N DIC E S

# A P P E N DIX  E

143
Appendix E : M apping T able— I& T -R elated Issues to G overnance and M anagem ent
O bjectives

Figure A .5— M apping I&T- R elated Issues to G overnance and M anagem ent O bjectives

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

144

Figure A .5— M apping I&T- R elated Issues to G overnance and M anagem ent O bjectives (cont.)

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

145

# A P P E N DIC E S

# A P P E N DIX  F

Appendix F: M apping T able— Threat Landscape to G overnance and M anagem ent
O bjectives

Figure A .6 — M apping Threat Landscape to G overnance and M anagem ent O bjectives
DF5 High N orm al

# EDM 01 3 .0 1.0

# EDM 02 1.0 1.0

# EDM 03 4.0 1.0

# EDM 04 1.0 1.0

# EDM 05 2.0 1.0

# A PO 01 3 .0 1.0

# A PO 02 1.0 1.0

# A PO 03 3 .0 1.0

# A PO 04 1.0 1.0

# A PO 05 1.0 1.0

# A PO 06 1.0 1.0

# A PO 07 2.0 1.0

# A PO 08 1.0 1.0

# A PO 09 2.0 1.0

# A PO 10 3 .0 1.0

# A PO 11 2.0 1.0

# A PO 12 4.0 1.0

# A PO 13 4.0 1.0

# A PO 14 3 .0 1.0

# BA I01 1.0 1.0

# BA I02 1.0 1.0

# BA I03 1.0 1.0

# BA I04 2.0 1.0

# BA I05 1.0 1.0

# BA I06 3 .0 1.0

# BA I07 1.0 1.0

# BA I08 1.0 1.0

# BA I09 1.0 1.0

# BA I10 3 .0 1.0

# BA I11 1.0 1.0

# DSS01 1.0 1.0

# DSS02 3 .0 1.0

# DSS03 2.0 1.0

# DSS04 4.0 1.0

# DSS05 3 .0 1.0

# DSS06 3 .0 1.0

# M EA 01 3 .0 1.0

# M EA 02 2.0 1.0

# M EA 03 3 .0 1.0

# M EA 04 3 .0 1.0

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

146
Appendix G : M apping T able— C om pliance R equirem ents to G overnance and
M anagem ent O bjectives

Figure A .7 — M apping C om pliance R equirem ents to G overnance and M anagem ent O bjectives
DF6 High N orm al Low

# EDM 01 3 .0 2.0 1.0

# EDM 02 1.0 1.0 1.0

# EDM 03 4.0 2.0 1.0

# EDM 04 1.0 1.0 1.0

# EDM 05 1.5 1.0 1.0

# A PO 01 2.0 1.5 1.0

# A PO 02 1.0 1.0 1.0

# A PO 03 1.0 1.0 1.0

# A PO 04 1.0 1.0 1.0

# A PO 05 1.0 1.0 1.0

# A PO 06 1.0 1.0 1.0

# A PO 07 1.0 1.0 1.0

# A PO 08 1.0 1.0 1.0

# A PO 09 1.0 1.0 1.0

# A PO 10 1.5 1.0 1.0

# A PO 11 1.0 1.0 1.0

# A PO 12 4.0 2.0 1.0

# A PO 13 1.5 1.0 1.0

# A PO 14 2.0 1.5 1.0

# BA I01 1.0 1.0 1.0

# BA I02 1.0 1.0 1.0

# BA I03 1.0 1.0 1.0

# BA I04 1.0 1.0 1.0

# BA I05 1.0 1.0 1.0

# BA I06 1.0 1.0 1.0

# BA I07 1.0 1.0 1.0

# BA I08 1.0 1.0 1.0

# BA I09 1.0 1.0 1.0

# BA I10 1.0 1.0 1.0

# BA I11 1.0 1.0 1.0

# DSS01 1.0 1.0 1.0

# DSS02 1.0 1.0 1.0

# DSS03 1.0 1.0 1.0

# DSS04 1.5 1.0 1.0

# DSS05 2.0 1.0 1.0

# DSS06 1.0 1.0 1.0

# M EA 01 1.0 1.0 1.0

# M EA 02 1.0 1.0 1.0

# M EA 03 4.0 2.0 1.0

# M EA 04 3 .5 2.0 1.0

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

147

# A P P E N DIC E S

# A P P E N DIX  H

Appendix H : M apping T able— R ole of IT to G overnance and M anagem ent O bjectives

Figure A .8— M apping R ole of IT to G overnance and M anagem ent O bjectives

## DF7 Support Factory Turnaround Strategic

# EDM 01 1.0 2.0 1.5 4.0

# EDM 02 1.0 1.0 2.5 3 .0

# EDM 03 1.0 3 .0 1.0 3 .0

# EDM 04 1.0 1.0 1.0 2.0

# EDM 05 1.0 1.0 1.0 2.0

# A PO 01 1.0 1.5 1.5 2.5

# A PO 02 1.0 1.0 3 .0 3 .0

# A PO 03 1.0 1.0 2.0 2.0

# A PO 04 0.5 1.0 3 .5 4.0

# A PO 05 1.0 1.0 2.5 3 .0

# A PO 06 1.0 1.0 1.0 2.0

# A PO 07 1.0 1.0 1.0 1.5

# A PO 08 1.0 1.0 2.0 2.5

# A PO 09 1.0 2.0 1.5 2.0

# A PO 10 1.0 2.5 1.5 2.0

# A PO 11 1.0 1.5 1.5 2.0

# A PO 12 1.0 2.5 1.0 3 .0

# A PO 13 1.0 2.0 1.5 3 .0

# A PO 14 1.0 1.5 1.5 2.5

# BA I01 1.0 1.0 2.0 2.5

# BA I02 1.0 1.0 3 .0 3 .0

# BA I03 1.0 1.0 3 .0 3 .0

# BA I04 1.0 2.5 1.5 2.0

# BA I05 1.0 1.0 1.0 2.0

# BA I06 1.0 2.5 1.0 2.0

# BA I07 1.0 1.0 2.0 2.0

# BA I08 1.0 1.0 1.0 2.0

# BA I09 1.0 1.0 1.0 2.0

# BA I10 1.0 1.5 1.0 2.0

# BA I11 1.0 1.0 2.0 2.0

# DSS01 1.0 3 .5 1.0 3 .0

# DSS02 1.0 3 .0 1.5 3 .0

# DSS03 1.0 3 .0 1.5 3 .5

# DSS04 1.0 3 .0 1.5 3 .5

# DSS05 1.5 2.5 1.5 3 .5

# DSS06 1.0 1.0 1.0 2.5

# M EA 01 1.0 1.0 1.0 2.0

# M EA 02 1.0 1.0 1.0 2.0

# M EA 03 1.0 1.0 1.0 1.5

# M EA 04 1.0 1.0 1.0 2.0

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

148
Appendix I: M apping T able— Sourcing M odel for IT to G overnance and M anagem ent
O bjectives

Figure A .9 — M apping Sourcing M odel for IT to G overnance and M anagem ent O bjectives
DF8 O utsourcing C loud Insourcing

# EDM 01 1.0 1.0 1.0

# EDM 02 1.0 1.0 1.0

# EDM 03 1.0 2.0 1.0

# EDM 04 1.0 1.0 1.0

# EDM 05 1.0 1.0 1.0

# A PO 01 1.0 1.0 1.0

# A PO 02 1.0 1.0 1.0

# A PO 03 1.0 1.0 1.0

# A PO 04 1.0 1.0 1.0

# A PO 05 1.0 1.0 1.0

# A PO 06 1.0 1.0 1.0

# A PO 07 1.0 1.0 1.0

# A PO 08 1.0 1.0 1.0

# A PO 09 4.0 4.0 1.0

# A PO 10 4.0 4.0 1.0

# A PO 11 1.0 1.0 1.0

# A PO 12 2.0 2.0 1.0

# A PO 13 1.0 1.0 1.0

# A PO 14 1.0 1.0 1.0

# BA I01 1.0 1.0 1.0

# BA I02 1.0 1.0 1.0

# BA I03 1.0 1.0 1.0

# BA I04 1.0 1.0 1.0

# BA I05 1.0 1.0 1.0

# BA I06 1.0 1.0 1.0

# BA I07 1.0 1.0 1.0

# BA I08 1.0 1.0 1.0

# BA I09 1.0 1.0 1.0

# BA I10 1.0 1.0 1.0

# BA I11 1.0 1.0 1.0

# DSS01 1.0 1.0 1.0

# DSS02 1.0 1.0 1.0

# DSS03 1.0 1.0 1.0

# DSS04 1.0 1.0 1.0

# DSS05 1.0 1.0 1.0

# DSS06 1.0 1.0 1.0

# M EA 01 3 .0 3 .0 1.0

# M EA 02 1.0 1.0 1.0

# M EA 03 1.0 1.0 1.0

# M EA 04 1.0 1.0 1.0

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

149

# A P P E N DIC E S

# A P P E N DIX  J

Appendix J:  M apping T able— IT Im plem entation M ethods to G overnance and
M anagem ent O bjectives

Figure A .10— M apping IT Im plem entation M ethods to G overnance and M anagem ent O bjectives
DF9 A gile DevO ps Traditional

# EDM 01 1.0 1.0 1.0

# EDM 02 1.0 1.0 1.0

# EDM 03 1.0 1.0 1.0

# EDM 04 1.0 1.0 1.0

# EDM 05 1.0 1.0 1.0

# A PO 01 1.0 1.0 1.0

# A PO 02 1.0 1.0 1.0

# A PO 03 1.0 2.0 1.0

# A PO 04 1.0 1.0 1.0

# A PO 05 1.0 1.0 1.0

# A PO 06 1.0 1.0 1.0

# A PO 07 1.0 1.5 1.0

# A PO 08 1.0 1.0 1.0

# A PO 09 1.0 1.0 1.0

# A PO 10 1.0 1.0 1.0

# A PO 11 1.0 1.0 1.0

# A PO 12 1.0 1.5 1.0

# A PO 13 1.0 1.0 1.0

# A PO 14 1.0 1.0 1.0

# BA I01 2.0 1.5 1.0

# BA I02 3 .5 2.0 1.0

# BA I03 4.0 3 .0 1.0

# BA I04 1.0 1.0 1.0

# BA I05 2.5 1.5 1.0

# BA I06 3 .5 2.0 1.0

# BA I07 2.5 2.5 1.0

# BA I08 1.0 1.0 1.0

# BA I09 1.0 1.0 1.0

# BA I10 1.5 2.0 1.0

# BA I11 2.5 1.0 1.0

# DSS01 1.0 2.5 1.0

# DSS02 1.0 1.5 1.0

# DSS03 1.0 1.5 1.0

# DSS04 1.0 1.0 1.0

# DSS05 1.0 1.0 1.0

# DSS06 1.0 1.0 1.0

# M EA 01 1.5 1.5 1.0

# M EA 02 1.0 1.0 1.0

# M EA 03 1.0 1.0 1.0

# M EA 04 1.0 1.0 1.0

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2 0 19 DE SIG N  G U IDE

150
Appendix K : M apping T able— T echnology A doption Strategies to G overnance and
M anagem ent O bjectives

Figure A .11— M apping Technology A doption Strategies to G overnance and M anagem ent O bjectives
DF10 First M over Follow er Slow  A dopter

# EDM 01 3 .5 2.5 1.5

# EDM 02 4.0 2.5 1.5

# EDM 03 1.5 1.0 1.0

# EDM 04 2.5 2.0 1.5

# EDM 05 1.5 1.0 1.0

# A PO 01 2.5 1.5 1.0

# A PO 02 4.0 3 .0 1.5

# A PO 03 2.0 1.0 1.0

# A PO 04 4.0 3 .0 1.0

# A PO 05 4.0 2.5 1.0

# A PO 06 1.0 1.5 1.0

# A PO 07 2.5 1.0 1.0

# A PO 08 3 .0 1.5 1.0

# A PO 09 1.5 1.5 1.0

# A PO 10 2.5 1.5 1.0

# A PO 11 1.5 1.5 1.0

# A PO 12 2.0 1.5 1.0

# A PO 13 1.0 1.0 1.0

# A PO 14 2.5 2.0 1.0

# BA I01 4.0 3 .0 1.5

# BA I02 3 .5 2.5 1.0

# BA I03 4.0 2.5 1.0

# BA I04 1.5 1.5 1.0

# BA I05 3 .0 2.0 1.0

# BA I06 2.5 2.0 1.0

# BA I07 3 .5 2.5 1.0

# BA I08 1.5 1.0 1.0

# BA I09 1.0 1.0 1.0

# BA I10 1.5 1.0 1.0

# BA I11 3 .5 2.5 1.0

# DSS01 1.0 1.0 1.0

# DSS02 1.0 1.0 1.0

# DSS03 1.5 1.0 1.0

# DSS04 1.5 1.0 1.0

# DSS05 1.5 1.0 1.0

# DSS06 1.0 1.0 1.0

# M EA 01 3 .0 2.0 1.0

# M EA 02 1.0 1.0 1.0

# M EA 03 1.0 1.0 1.0

# M EA 04 1.0 1.0 1.0

## Personal Copy of Andrew Hana (ISACA ID: 1571067)