---
title: COBIT-2019-Implementation-Guide_res_eng_1218
date: "2018-11-13T13:08:14"
source: COBIT-2019-Implementation-Guide_res_eng_1218.pdf
format: pdf
---

# IMPLEMENTATION GUIDE

## Implementing and

## Optimizing an Information

## and Technology

## Governance Solution

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

## A bout ISA C A

Nearing its 50th year, ISA C A ® (isaca.org) is a global association helping individuals and enterprises achieve the
positive potential of technology. Technology pow ers today’s w orld and ISA C A  equips professionals w ith the
know ledge, credentials, education and com m unity to advance their careers and transform  their organizations. ISA C A
leverages the expertise of its half-m illion engaged professionals in inform ation and cyber security, governance,
assurance, risk and innovation, as w ell as its enterprise perform ance subsidiary, C M M I ® Institute, to help advance
innovation through technology. ISA C A  has a presence in m ore than 188 countries, including m ore than 217 chapters
and offices in both the U nited States and C hina.
Disclaim er
ISA C A  has designed and created C O BIT ® 201 9 Im plem entation G uide: Im plem enting and O ptim izing an Inform ation
and Technology G overnance Solution (the “W ork”) prim arily as an educational resource for enterprise governance of
inform ation and technology (EGIT), assurance, risk and security professionals. ISA C A  m akes no claim  that use of
any of the W ork w ill assure a successful outcom e. The W ork should not be considered inclusive of all proper
inform ation, procedures and tests or exclusive of other inform ation, procedures and tests that are reasonably directed
to obtaining the sam e results. In determ ining the propriety of any specific inform ation, procedure or test, enterprise
governance of inform ation and technology (EGIT), assurance, risk and security professionals should apply their ow n
professional judgm ent to the specific circum stances presented by the particular system s or inform ation technology
environm ent.
C opyright
©  2018 ISA C A . A ll rights reserved. For usage guidelines, see w w w.isaca.org/C O BITuse .

# ISA C A

1700 E. Golf R oad, Suite 400
Schaum burg, IL 6 0173, U SA
Phone: +1.847.6 6 0.5505
Fax: +1.847.253.1755
C ontact us: https://support.isaca.org
W ebsite: w w w .isaca.org
Participate in the ISA C A  O nline Forum s: https://engage.isaca.org/onlineforum s
Tw itter: http://tw itter.com /ISA C A New s
L inkedIn: http://linkd.in/ISA C A O fficial
Facebook: w w w .facebook.com /ISA C A H Q
Instagram : w w w .instagram .com /isacanew s/

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

2
C O BIT ® 201 9 Im plem entation G uide: Im plem enting and O ptim izing an Inform ation and Technology G overnance Solution

# ISB N 9 78-1-6 0420-76 6 -8

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

3

# IN  M E M O R IA M : JO H N  LA IN H A R T (1946-2018)

In M em oriam : John Lainhart (1946-2 018)
D edicated to John Lainhart, ISA C A  B oard chair 19 84-19 85. John w as instrum ental in the creation of the C O B IT ®
fram ew ork and m ost recently served as chair of the w orking group for C O B IT ® 2019 , w hich culm inated in the
creation of this w ork. O ver his four decades w ith ISA C A , John w as involved in num erous aspects of the association
as w ell as holding ISA C A’s C ISA , C R ISC , C ISM  and C GEIT certifications. John leaves behind a rem arkable
personal and professional legacy, and his efforts significantly im pacted ISA C A .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

P age intentionally left blank
4

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

A cknow ledgm ents
ISAC A w ishes to recognize:
CO B IT W orking G roup (2017-2018)
John Lainhart, C hair, C ISA, C R ISC , C ISM , C G E IT, C IPP/G , C IPP/U S, G rant Thornton, U SA
M att C onboy, C igna, U SA
R on Saull, C G E IT, C SP, G reat-W est Lifeco & IG M  Financial (retired), C anada
Developm ent T eam
Steven D e H aes, Ph.D ., Antw erp M anagem ent School, U niversity of Antw erp, B elgium
M atthias G oorden, Pw C , B elgium
Stefanie G rijp, Pw C , B elgium
B art Peeters, Pw C , B elgium
G eert Poels, Ph.D ., G hent U niversity, B elgium
D irk Steuperaert, C ISA, C R ISC , C G E IT, IT In B alance, B elgium
Expert R eview ers
Floris Am pe, C ISA, C R ISC , C G E IT, C IA, ISO 270 0 0 , PR IN C E 2, TO G AF, Pw C , B elgium

## G raciela B raga, C G E IT, Auditor and Advisor, Argentina

Jam es L. G olden, G olden C onsulting Associates, U SA
J. W inston H ayden, C ISA, C R ISC , C ISM , C G E IT, South Africa
Abdul R afeq, C ISA, C G E IT, FC A, M anaging D irector, W incer Infotech Lim ited, India
Jo Stew art-R attray, C ISA, C R ISC , C ISM , C G E IT, FAC S C P, B R M  H oldich, Australia

## ISA CA  B oard of D irectors

R ob C lyde, C ISM , C lyde C onsulting LLC , U SA, C hair
B rennan B aybeck, C ISA, C R ISC , C ISM , C ISSP, O racle C orporation, U SA, V ice-C hair
Tracey D edrick, Form er C hief R isk O fficer w ith H udson C ity B ancorp, U SA
Leonard O ng, C ISA, C R ISC , C ISM , C G E IT, C O B IT 5 Im plem enter and Assessor, C FE , C IPM , C IPT, C ISSP,
C ITB C M , C PP, C SSLP, G C FA, G C IA, G C IH , G SN A, ISSM P-ISSAP, PM P, M erck & C o., Inc., Singapore
R .V . R aghu, C ISA, C R ISC , Versatilist C onsulting India Pvt. Ltd., India
G abriela R eynaga, C ISA, C R ISC , C O B IT 5 Foundation, G R C P, H olistics G R C , M exico

## G regory Touhill, C ISM , C ISSP, C yxtera Federal G roup, U SA

## Ted W olff, C ISA, Vanguard, Inc., U SA

Tichaona Zororo, C ISA, C R ISC , C ISM , C G E IT, C O B IT 5 Assessor, C IA, C R M A, E G IT | E nterprise G overnance

## of IT, South Africa

Theresa G rafenstine, C ISA, C R ISC , C G E IT, C G AP, C G M A, C IA, C ISSP, C PA, D eloitte & Touche LLP, U SA,
ISAC A B oard C hair, 20 17-20 18
C hris K . D im itriadis, Ph.D ., C ISA, C R ISC , C ISM , IN TR ALO T, G reece, ISAC A B oard C hair, 20 15-20 17
M att Loeb, C G E IT, C AE , FASAE , C hief E xecutive O fficer, ISAC A, U SA
R obert E  Stroud (196 5-20 18), C R ISC , C G E IT, X ebiaLabs, Inc., U SA, ISAC A B oard C hair, 20 14 -20 15
ISA C A  is deeply saddened by the passing of R obert E  Stroud in Septem ber 2018.

# A C K N O W LED G M EN TS

5

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

P age intentionally left blank
6

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# T A B LE O F C O N TEN TS

List of Figures ...................................................................................................................................................9
C hapter 1 . Introduction ..........................................................................................................................1 1
1.1 Im provem ent of E nterprise Governance of Inform ation and Technology ........................................................11
1.2 C O B IT O verview .........................................................................................................................................12
1.3 O bjectives and Scope of the Im plem entation Guide .......................................................................................12
1.4 Structure of T his P ublication ........................................................................................................................13
1.5 Target A udience for T his P ublication ............................................................................................................14
1.6  R elated Guidance: C O BIT ® 2019 D esign G uide ............................................................................................14
C hapter 2 . Positioning Enterprise G overnance of I&T ...........................................1 5
2.1 U nderstanding the C ontext ...........................................................................................................................15
2.1.1 W hat is E GIT ? .....................................................................................................................................15
2.1.2 W hy is E GIT so Im portant? ..................................................................................................................16
2.1.3 W hat Should E GIT D eliver? .................................................................................................................17
2.2 Leveraging C O B IT and Integrating Fram ew orks, Standards and Good P ractices ............................................17
2.2.1 Governance P rinciples .........................................................................................................................18
2.2.2 Governance System  and C om ponents ....................................................................................................20
2.2.3 Governance and M anagem ent O bjectives ...............................................................................................20
C hapter 3 . Taking the First Steps Tow ard EG IT ............................................................21
3.1 C reating the A ppropriate E nvironm ent ..........................................................................................................21
3.2 A pplying a C ontinual Im provem ent Life C ycle A pproach ..............................................................................23
3.2.1 P hase 1— W hat A re the D rivers? ...........................................................................................................24
3.2.2 P hase 2— W here A re W e Now ? ..............................................................................................................24
3.2.3 P hase 3— W here D o W e W ant to B e? .....................................................................................................25
3.2.4 P hase 4— W hat Needs to B e D one? .......................................................................................................25
3.2.5 P hase 5— H ow  D o W e Get T here? .........................................................................................................25
3.2.6  P hase 6 — D id W e Get T here? ................................................................................................................25
3.2.7 P hase 7— H ow  D o W e K eep the M om entum  Going? ................................................................................25
3.3 Getting Started— Identify the Need to A ct: R ecognizing P ain P oints and Trigger E vents ................................26
3.3.1 Typical P ain P oints ...............................................................................................................................26
3.3.2 Trigger E vents in the Internal and E xternal E nvironm ents .......................................................................28
3.3.3 Stakeholder Involvem ent ......................................................................................................................30
3.4 R ecognizing Stakeholders’ R oles and R equirem ents ......................................................................................30
3.4.1 Internal Stakeholders ............................................................................................................................30
3.4.2 E xternal Stakeholders ...........................................................................................................................32
3.4.3 Independent A ssurance and the R ole of A uditors ....................................................................................33
C hapter 4 . Identifying C hallenges and Success Factors .....................................35
4.1 Introduction .................................................................................................................................................35
4.2 C reating the A ppropriate E nvironm ent ..........................................................................................................35
4.2.1 P hase 1— W hat A re the D rivers? ...........................................................................................................35
4.2.2 P hase 2— W here A re W e Now ? and P hase 3— W here D o W e W ant to B e? .................................................37
4.2.3 P hase 4— W hat Needs to B e D one? .......................................................................................................38
4.2.4 P hase 5— H ow  D o W e Get T here? .........................................................................................................40
4.2.5 P hase 6 — D id W e Get T here? and P hase 7— H ow  D o W e K eep the M om entum  Going? ..............................41
C hapter 5 . Enabling C hange .............................................................................................................4 3
5.1 T he Need for C hange E nablem ent .................................................................................................................43
5.1.1 C hange E nablem ent of E GIT Im plem entation .........................................................................................44

# T A B LE  O F  C O N TE N TS

7

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

5.2 P hases in the C hange E nablem ent Life C ycle C reate the A ppropriate E nvironm ent ........................................45
5.2.1 P hase 1— E stablish the D esire to C hange ...............................................................................................45
5.2.2 P hase 2— Form  an E ffective Im plem entation Team .................................................................................45
5.2.3 P hase 3— C om m unicate D esired V ision ..................................................................................................46
5.2.4 P hase 4— E m pow er R ole P layers and Identify Q uick W ins ......................................................................46
5.2.5 P hase 5— E nable O peration and U se ......................................................................................................46
5.2.6  P hase 6 — E m bed New  A pproaches ........................................................................................................47
5.2.7 P hase 7— Sustain .................................................................................................................................47
C hapter 6 . Im plem entation Life C ycle ...................................................................................4 9
6 .1 Introduction .................................................................................................................................................49
6 .2 P hase 1— W hat A re the D rivers? ...................................................................................................................50
6 .3 P hase 2— W here A re W e Now ? .....................................................................................................................53
6 .4 P hase 3— W here D o W e W ant to B e? ............................................................................................................57
6 .5 P hase 4— W hat Needs to B e D one? ...............................................................................................................6 0
6 .6  P hase 5— H ow  D o W e Get T here? .................................................................................................................6 4
6 .7 P hase 6 — D id W e Get T here? ........................................................................................................................6 7
6 .8 P hase 7— H ow  D o W e K eep the M om entum  Going? ......................................................................................70
A ppendix A . Exam ple D ecision M atrix ..................................................................................73
8

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# LIST O F FIG U R ES

C hapter 1 . Introduction
Figure 1.1— T he C ontext of E nterprise Governance of Inform ation and Technology ...................................................11
Figure 1.2— C O B IT O verview ..................................................................................................................................12
C hapter 2 . Positioning Enterprise G overnance of I&T
Figure 2.1— Governance System  P rinciples ...............................................................................................................19
Figure 2.2— Governance Fram ew ork P rinciples .........................................................................................................19
C hapter 3 . Taking the First Steps Tow ard EG IT
Figure 3.1— R oles in C reating the A ppropriate E nvironm ent .....................................................................................22
Figure 3.2— R esponsibilities of Im plem entation R ole P layers ....................................................................................22
Figure 3.3— A pplying a C ontinual Im provem ent Life C ycle A pproach .......................................................................23
Figure 3.4— C O B IT Im plem entation R oad M ap .........................................................................................................24
Figure 3.5— O verview  of Internal E GIT Stakeholders ................................................................................................31
Figure 3.6 — O verview  of E xternal E GIT Stakeholders ...............................................................................................32
C hapter 4 . Identifying C hallenges and Success Factors
Figure 4.1— C hallenges, R oot C auses and Success Factors for P hase 1 ......................................................................35
Figure 4.2— C hallenges, R oot C auses and Success Factors for P hases 2 and 3 ...........................................................37
Figure 4.3— C hallenges, R oot C auses and Success Factors for P hase 4 ......................................................................38
Figure 4.4— C hallenges, R oot C auses and Success Factors for P hase 5 ......................................................................40
Figure 4.5— C hallenges, R oot C auses and Success Factors for P hases 6  and 7 ...........................................................41
C hapter 5 . Enabling C hange
Figure 5.1— C hange E nablem ent Life C ycle ..............................................................................................................44
C hapter 6 . Im plem entation Life C ycle
Figure 6 .1— P hase 1 W hat A re the D rivers? ...............................................................................................................50
Figure 6 .2— P hase 1 R oles ........................................................................................................................................50
Figure 6 .3— P hase 1 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs .................................................51
Figure 6 .4— P hase 1 R A C I C hart ..............................................................................................................................52
Figure 6 .5— P hase 2 W here A re W e Now ? .................................................................................................................53
Figure 6 .6 — P hase 2 R oles ........................................................................................................................................53
Figure 6 .7— P hase 2 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs .................................................53
Figure 6 .8— P hase 2 R A C I C hart ..............................................................................................................................56
Figure 6 .9 — P hase 3 W here D o W e W ant to B e? ........................................................................................................57
Figure 6 .10— P hase 3 R oles ......................................................................................................................................57
Figure 6 .11— P hase 3 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs ...............................................58
Figure 6 .12— P hase 3 R A C I C hart ............................................................................................................................6 0
Figure 6 .13— P hase 4 W hat Needs to B e D one? .........................................................................................................6 0
Figure 6 .14— P hase 4 R oles ......................................................................................................................................6 1
Figure 6 .15— P hase 4 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs ...............................................6 1
Figure 6 .16 — P hase 4 R A C I C hart ............................................................................................................................6 3
Figure 6 .17— P hase 5 H ow  D o W e Get T here? ...........................................................................................................6 4
Figure 6 .18— P hase 5 R oles ......................................................................................................................................6 4
Figure 6 .19 — P hase 5 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs ...............................................6 5
Figure 6 .20— P hase 5 R A C I C hart ............................................................................................................................6 6
Figure 6 .21— P hase 6  D id W e Get T here? ..................................................................................................................6 7
Figure 6 .22— P hase 6  R oles ......................................................................................................................................6 7
Figure 6 .23— P hase 6  O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs ...............................................6 8
Figure 6 .24— P hase 6  R A C I C hart ............................................................................................................................6 9
Figure 6 .25— P hase 7 H ow  D o W e K eep the M om entum  Going? ................................................................................70

# LIST O F  F IGU R E S

9

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

Figure 6 .26 — P hase 7 R oles ......................................................................................................................................70
Figure 6 .27— P hase 7 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs ...............................................71
Figure 6 .28— P hase 7 R A C I C hart ............................................................................................................................72
A ppendix A . Exam ple D ecision M atrix
Figure A .1— E xam ple D ecision M atrix ......................................................................................................................73
10

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

11

# C H A P TE R  1

# IN TR O DU C TIO N

C hapter 1
Introduction
1.1  Im provem ent of E nterprise Governance of Inform ation and T echnology
In the light of digital transform ation, inform ation and technology (I& T) 1
1 have becom e crucial in the support,
sustainability and grow th of enterprises. Previously, governing boards (boards of directors) and senior m anagem ent
could delegate, ignore or avoid I& T-related decisions. In m ost sectors and industries, such attitudes are now  ill-
advised. Stakeholder value creation (i.e., realizing benefits at an optim al resource cost w hile optim izing risk) is often
driven by a high degree of digitization in new  business m odels, efficient processes, successful innovation, etc.
D igitized enterprises are increasingly dependent on I& T for survival and grow th.
Given the centrality of I& T for enterprise risk m anagem ent and value generation, a specific focus on enterprise
governance of inform ation and technology (EGIT) has arisen over the last three decades. EGIT is an integral part of
corporate governance. It is exercised by the board that oversees the definition and im plem entation of processes,
structures and relational m echanism s in the organization that enable both business and IT people to execute their
responsibilities in support of business/IT alignm ent and the creation of business value from  I& T-enabled business
investm ents ( figure 1.1 ).

For m any years, ISA C A ® has researched this key area of enterprise governance to advance international thinking and
provide guidance in evaluating, directing and m onitoring an enterprise’s use of I& T. ISA C A  has developed the
C O B IT ® fram ew ork to help enterprises im plem ent sound governance and m anagem ent com ponents. Indeed,
im plem enting good EGIT is alm ost im possible w ithout using an effective governance fram ew ork.
Effective EGIT w ill im prove business perform ance and com pliance w ith external requirem ents. Yet, successful
im plem entation still eludes m any enterprises. EGIT is com plex and m ultifaceted. There is no silver bullet (or ideal
w ay) to design, im plem ent and m aintain effective EGIT w ithin an organization. A s such, m em bers of the governing
boards and senior m anagem ent typically need to tailor their EGIT m easures and im plem entation to their ow n specific
context and needs. They m ust also be w illing to accept m ore accountability for I& T and drive a different m indset and
culture for delivering value from  I& T.
1
1 Throughout this text, IT is used to refer to the organizational departm ent w ith m ain responsibility for technology. I& T as used in this text refers to all
the inform ation the enterprise generates, processes and uses to achieve its goals, as w ell as the technology to support that throughout the enterprise.
Figure 1 .1 — The Context of Enterprise G overnance of Inform ation and Technology
Enterprise

## Governance of IT

## Business/I T

Alignment
Value
Creation
Source: De Haes, Steven; W. Van Grembergen; Enterprise G overnance of Inform ation Technology: A chieving A lignm ent and V alue,
Featuring C O B IT 5 , 2 nd ed., Springer International Publishing, Switzerland, 2015, https://w w w .springer.com /us/book/978331 91 45 464

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 20 19 IM P LEM EN T A TIO N  G U ID E

12

## 1.2  C O B IT O verview

C O BIT ® 2019 Im plem entation G uide: Im plem enting and O ptim izing an Inform ation and Technology G overnance
Solution is the fourth publication in the C O B IT ® 2019 suite of products (see figu re 1.2 ). Som e of the other
publications are described below .
C O B IT ® 2019 F ram ew ork: Introduction and M ethodology introduces the key concepts of C O B IT ® 2019. 
C O B IT ® 2019 F ram ew ork: G overnance and M anagem ent O bjectives com prehensively describes the 40 core 
governance and m anagem ent objectives, the processes contained therein, and other related com ponents. T his guide
also references other standards and fram ew orks.
C O B IT ® 2019 D esign G uide: D esigning an Inform ation and Technology G overnance Solution explores design 
factors that can influence governance and includes a w orkflow  for planning a tailored governance system  for the
enterprise.
T he objective of this reference guide is to provide good practices for im plem enting and optim izing an I& T
governance system , based on a continual im provem ent life cycle approach, w hich should be tailored to suit the
enterprise’s specific needs.

1.3  O bjectives and Scope of the Im plem entation G uide
C O B IT  principles em phasize the enterprisew ide view  of governance of I& T  (see C O BIT ® 2019 Fram ew ork:
Introduction and M ethodology ). Inform ation and technology are not confined to the IT  departm ent; they are
pervasive throughout the enterprise. It is neither possible nor good practice to separate I& T-related activities from  the

## Figure 1.2— C O B IT O verview

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

13

# C H A P TE R  1

# IN TR O DU C TIO N

business. The governance and m anagem ent of enterprise I& T should, therefore, be im plem ented as an integral part of
enterprise governance, covering the full end-to-end business and IT functional areas of responsibility.
O ne of the com m on reasons w hy som e governance system  im plem entations fail is that they are not initiated and then
m anaged properly as program s to ensure that benefits are realized. Governance program s need to be sponsored by
executive m anagem ent, be properly scoped and define objectives that are attainable. This enables the enterprise to
absorb the pace of change as planned. Program  m anagem ent is, therefore, addressed as an integral part of the
im plem entation life cycle.
It is also assum ed that w hile a program  and project approach is recom m ended to effectively drive im provem ent
initiatives, the goal is also to establish a norm al business practice and sustainable approach to governing and
m anaging enterprise I& T just like any other aspect of enterprise governance. For this reason, the im plem entation
approach is based on em pow ering business and IT stakeholders and role players to take ow nership of IT-related
governance and m anagem ent decisions and activities by facilitating and enabling change. The im plem entation
program  is closed w hen the process for focusing on IT-related priorities and governance im provem ent is generating a
m easurable benefit, and the program  has becom e em bedded in ongoing business activity.
This publication is not intended to be a prescriptive approach or the com plete solution, but rather a guide to avoid
pitfalls, leverage the latest good practices, and assist in the creation of successful governance and m anagem ent
outcom es over tim e. To an im portant extent, it leverages the C O BIT ® 201 9 D esign G uide , w hich helps every
enterprise to identify and apply its ow n specific plan or road m ap, depending on a num ber of design factors such as
enterprise strategy, risk and threat issues, and role of IT.
D eterm ining the current starting point is equally im portant. Few  enterprises have no EGIT structures or processes in
place, even if they are not recognized as such currently. Therefore, the em phasis m ust be on building on w hat the
enterprise already has in place, especially leveraging existing successful enterprise-level approaches that can be
adopted, and, if necessary, adapted for I& T governance, rather than inventing som ething different. Furtherm ore, any
previous im provem ents created by applying C O B IT ® 5 or other standards and good practices need not be rew orked.
Instead, they can, and should be, enhanced by C O B IT ® 2019  as an ongoing part of continual im provem ent.
C O B IT ® 2019  is freely dow nloadable from  w w w.isaca.org/cobit . Links to ISA C A  products supporting
im plem entation are available on this page as w ell.
This publication reflects enhanced understanding of and practical experience w ith EGIT im plem entations, lessons
learned w hile applying and using previous versions of C O B IT, and updates m ade to ISA C A’s guidance. H ow ever,
I& T never stand still, so users of this guide should anticipate ISA C A’s professional publications and other
organizations’ standards and good practices that m ay be released from  tim e to tim e to address new ly em erging topics.
New , forthcom ing focus area content w ill becom e part of the C O B IT product fam ily and w ill provide im portant
guidance on these em erging topics. 2
2
1.4  Structure of This P ublication
The rem ainder of this publication contains the follow ing sections and appendices:
C hapter 2 explains the positioning of EGIT w ithin the enterprise. 
C hapter 3 discusses the first steps tow ard im proving EGIT. 
C hapter 4 describes im plem entation challenges and success factors. 
C hapter 5 covers EGIT-related organizational and behavioral change. 

2
2 A t the tim e of publication of this C O BIT ® 201 9 Im plem entation G uide , focus area content is planned, but not yet released.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

14
C hapter 6  describes the im plem entation life cycle, including change enablem ent and program  m anagem ent. 
The appendix provides an exam ple decision m atrix. 
1.5   T arget A udience for This P ublication
The target audience for this publication is experienced professionals throughout the enterprise, including business
departm ents, audit, security, privacy, risk m anagem ent, IT professionals, external professionals and others involved
(or planning to be involved) in the im plem entation of EGIT.
A  certain level of experience and a thorough understanding of the enterprise are required to benefit from  this guide.
Such experience and understanding allow  users to custom ize the core C O B IT guidance— w hich is generic in
nature— into tailored and focused guidance for the enterprise, taking into account the enterprise’s context.
1.6  R elated Guidance: CO BIT ® 2019 D esign G uide
The C O BIT ® 201 9 D esign G uide is related to this publication. It defines design factors that can influence a
governance system  and includes a w orkflow  for designing a tailored governance system  for the enterprise. The
w orkflow  explained in the C O BIT ® 201 9 D esign G uide has a num ber of connection points w ith the C O BIT ® 201 9
Im plem entation G uide; the design guide elaborates a set of tasks defined in this im plem entation guide.
C hapter 5 of the C O BIT ® 201 9 D esign G uide explores the links betw een the tw o publications and illustrates how  to
use them  together.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

15

# C H A P TE R  2

P O SITIO N IN G E N TE R P R ISE  GO V E R N A N C E  O F  I&T
C hapter 2

## Positioning E nterprise Governance of I&T

2.1  U nderstanding the C ontext
Enterprise governance of inform ation and technology (EGIT) does not occur in a vacuum . Im plem entation takes
place in different conditions and circum stances determ ined by num erous factors in the internal and external
environm ent, such as:
The com m unity’s ethics and culture 
Governing law s, regulations and policies 
International standards 
Industry practices 
The econom ic and com petitive environm ent 
Technology advancem ents and evolution 
The threat landscape 
The enterprise’s: 
R eason for existence, m ission, vision, goals and values 
Governance policies and practices 
C ulture and m anagem ent style 
M odels for roles and responsibilities 
B usiness plans and strategic intentions 
O perating m odel and level of m aturity 
The im plem entation of EGIT for each enterprise is, therefore, different, and the context needs to be understood and
considered to design the optim al new  or im proved EGIT environm ent. This is fully elaborated in the C O BIT ® 201 9
D esign G uide .
2.1.1  W hat is E GIT?
The term s governance, enterprise governance and EGIT m ay have different m eanings depending on organizational
context (m aturity, industry and regulatory environm ent) or individual context (job role, education and experience),
am ong other factors. Explanations in this chapter provide a foundation for the rest of the guide, but it should be
recognized that different points of view  do exist. It is better to build on and enhance existing approaches to include
I& T than to develop a new  approach just for I& T.
The term  governance derives from  the Greek verb kubernáo , m eaning “to steer.” A  governance system  enables
m ultiple stakeholders in an enterprise to have an organized say in evaluating conditions and options, setting
direction, and m onitoring perform ance against enterprise objectives. Setting and m aintaining the appropriate
governance approach are the responsibility of the board of directors or equivalent body.
C O B IT defines governance as follow s:
G overnance ensures that stakeholder needs, conditions and options are evaluated to determ ine balanced,
agreed-on enterprise objectives to be achieved; setting direction through prioritization and decision m aking;
and m onitoring perform ance and com pliance against agreed-on direction and objectives. 3
3    See C O BIT ® 201 9 Fram ew ork: Introduction and M ethodology , Section 1.3.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

16
EGIT is not an isolated discipline, but an integral part of enterprise governance. The need for governance at an
enterprise level is driven prim arily by delivery of stakeholder value and dem and for transparency and effective
m anagem ent of enterprise risk. The significant opportunities, costs and risk associated w ith I& T call for a dedicated,
yet integrated, focus on EGIT. EGIT enables the enterprise to take full advantage of I& T, m axim izing benefits,
capitalizing on opportunities and gaining com petitive advantage.
2.1.2  W hy is E GIT so Im portant?
Globally, enterprises— w hether public or private, large or sm all— increasingly understand that inform ation is a key
resource and technology is a strategic asset, both critical to success.
I& T can be pow erful resources to help enterprises achieve their m ost im portant objectives. For exam ple, I& T can
drive cost savings for large transactions such as m ergers, acquisitions and divestitures. I& T can enable autom ation of
key processes, such as the supply chain. I& T can be the cornerstone of new  business strategies or business m odels,
thereby increasing com petitiveness and enabling innovation, such as digital delivery of products (e.g., m usic sold
and delivered online). I& T can enable greater custom er intim acy, for exam ple, by collating and m ining data in
diverse system s and providing a 36 0-degree view  of custom ers. I& T are the foundation of the netw orked econom y
that cuts through geographic locations and organizational silos to provide new  and innovative w ays of creating value.
M ost enterprises recognize inform ation and the use of I& T as critical assets that need to be governed properly.
W hile I& T has the potential for business transform ation, it often represents a very significant investm ent at the sam e
tim e. In m any cases, true IT cost is not transparent, and budgets are spread across business units, functions and
geographic locations, w ithout central oversight. The greatest portion of spending often just keeps the lights on,
funding m aintenance and operations post-im plem entation, rather than innovative or transform ational initiatives.
W hen funds are spent on strategic initiatives, they often fail to deliver expected outcom es. M any enterprises still fail
to dem onstrate concrete, m easurable business value for IT-enabled investm ents and focus on EGIT as a m echanism
to address this situation.
The netw orked econom y presents a spectrum  of IT-related risk, including com prom ise of custom er-facing business
system s, disclosure of custom er or proprietary data, or m issed business opportunities due to inflexible IT
architecture. M anaging these and other types of I& T-related risk is another driver for better EGIT.
EGIT can address the com plex regulatory environm ent faced by enterprises in m any industries and jurisdictions
today, often extending directly to IT. R equirem ents and scrutiny around financial reporting drive significant focus on
IT-related controls. The use of good practices such as C O B IT has been m andated in som e countries and industries.
For exam ple, the B anking R egulation and Supervision A gency (B R SA ) of Turkey has m andated that all banks
operating in Turkey m ust adopt C O B IT’s good practices w hen m anaging IT-related processes, as has the A ustralian
Prudential R egulation A uthority. The report on corporate governance in South A frica— K ing IV — includes a
principle to im plem ent EGIT and recom m ends the adoption of fram ew orks such as C O B IT. A  governance fram ew ork
for I& T can facilitate com pliance in a m ore effective and efficient w ay.
R esearch has long dem onstrated the value of EGIT.  In a large case study of an international airline com pany, EGIT’s
benefits w ere dem onstrated to include: low er IT-related continuity costs, increased IT-enabled innovation capacity,
increased alignm ent betw een digital investm ents and business goals and strategy, increased trust betw een business
and IT, and a shift tow ard a “value m indset” around digital assets. 4
1
1
4 D e H aes, S.; W . van Grem bergen; Enterprise G overnance of IT: Achieving Alignm ent and Value, Featuring C O BIT 5 , 2 nd ed., Springer International
Publishing, Sw itzerland, 2015, https://w w w.springer.com /us/book/978 331 91 45464

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

17

# C H A P TE R  2

P O SITIO N IN G E N TE R P R ISE  GO V E R N A N C E  O F  I&T
R esearch has show n that enterprises w ith poorly designed or adopted approaches to EGIT perform  w orse in aligning
business and I& T strategies and processes. A s a result, such enterprises are m uch less likely to achieve  their
intended business strategies and realize the business value they expect from  digital transform ation. 5
2
From  this, it is clear that governance has to be understood and im plem ented m uch beyond the often encountered (i.e.,
narrow ) interpretation suggested by the governance, risk and com pliance (GR C ) acronym . The GR C  acronym  itself
im plicitly suggests that com pliance and related risk represent the spectrum  of governance.
2.1.3   W hat Should E GIT Deliver?
Fundam entally, EGIT is concerned w ith value delivery from  digital transform ation and the m itigation of business
risk that results from  digital transform ation. M ore specifically, three m ain outcom es can be expected after successful
adoption of EGIT:
Benefits realization — This consists of creating value for the enterprise through I& T, m aintaining and increasing 
value derived from  existing I& T 6
3 investm ents, and elim inating IT initiatives and assets that are not creating
sufficient value. The basic principle of I& T value are delivery of fit-for-purpose services and solutions, on tim e
and w ithin budget, that generate the intended financial and nonfinancial benefits. The value that I& T delivers
should be aligned directly w ith the values on w hich the business is focused. IT value should also be m easured in a
w ay that show s the im pact and contributions of IT-enabled investm ents in the value creation process of the
enterprise.
Risk optim ization — This entails addressing the business risk associated w ith the use, ow nership, operation, 
involvem ent, influence and adoption of I& T w ithin an enterprise. I& T-related business risk consists of I& T-related
events that could potentially im pact the business. W hile value delivery focuses on the creation of value, risk
m anagem ent focuses on the preservation of value. The m anagem ent of I& T-related risk should be integrated w ithin
the enterprise risk m anagem ent approach to ensure a focus on IT by the enterprise. It should also be m easured in a
w ay that show s the im pact and contributions of optim izing I& T-related business risk on preserving value.
Resource optim ization — This ensures that the appropriate capabilities are in place to execute the strategic plan 
and sufficient, appropriate and effective resources are provided. R esource optim ization ensures that an integrated,
econom ical IT infrastructure is provided, new  technology is introduced as required by the business, and obsolete
system s are updated or replaced. B ecause it recognizes the im portance of people, in addition to hardw are and
softw are, it focuses on providing training, prom oting retention and ensuring com petence of key IT personnel. A n
im portant resource is data and inform ation, and exploiting data and inform ation to gain optim al value is another
key elem ent of resource optim ization.
Throughout im plem entation and exercise of EGIT, strategic alignm ent and perform ance m easurem ent are of
param ount im portance and apply overall to all activities to ensure that I& T-related objectives are aligned w ith the
enterprise goals.
2.2  Leveraging C O B IT and Integrating F ram ew orks, Standards and Good P ractices
C O B IT is based on an enterprise view , and it  aligns w ith enterprise governance good practices. C O B IT is a single,
overarching fram ew ork w hose consistent, integrated guidance is expressed in nontechnical and technology-agnostic
language. The board should m andate adoption of an EGIT fram ew ork like C O B IT as an essential part of enterprise
governance developm ent.
2
5 D e H aes S.; A . Joshi; W . van Grem bergen; “State and Im pact of Governance of Enterprise IT in O rganizations: K ey Findings of an International
Study,” ISAC A ® Journal , vol. 4, 2015, https://w w w.isaca.org/Journal/archives/201 5/Volum e-4/Pages/state-and-im pact-of-governance-of-enterprise-
itin-organizations.aspx . See also op cit D e H aes and van Grem bergen, Enterprise G overnance of IT: Achieving Alignm ent and Value, Featuring

# C O BIT 5.

3
6 Throughout this text, IT is used to refer to the organizational departm ent w ith m ain responsibility for technology. I& T as used in this text refers to all
the inform ation the enterprise generates, processes and uses to achieve its goals, as w ell as the technology to support that throughout the enterprise.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

18
W orking w ithin a fram ew ork and leveraging good practices enables developm ent and optim ization of appropriate
governance processes and other com ponents of the governance system . Tailored appropriately, EGIT w ill operate
effectively as part of an enterprise’s norm al business practice, provided there is a supporting culture, dem onstrated
by top m anagem ent.
C O B IT ® 2019  not only outlines a general approach, but also references other detailed standards. C O BIT ® 201 9
Fram ew ork: Introduction and M ethodology , C hapter 10, lists  all standards that align to C O B IT ® 2019 ; these
standards  reappear, elaborated by detailed references, under the governance and m anagem ent objectives, their
associated practices, and com ponents in C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives .
A ligning w ith C O B IT should also result in faster and m ore efficient external audits since C O B IT is w idely accepted
as a basis for IT audit procedures.
The C O B IT fram ew ork sets out the overall approach; guidance provided by specific standards and good practices
can then be applied to specific processes, practices, policies and procedures, as the enterprise tailors its
im plem entation. Specifically, the governance system  and its com ponents should align and harm onize w ith the:
Enterprise policies, strategies, governance and business plans, and audit approaches 
Enterprise risk m anagem ent (ER M ) fram ew ork 
Existing enterprise governance organization, structures and processes 
2.2.1  Governance P rinciples
C O B IT ® 2019  w as developed based on tw o sets of principles:
Principles that describe the core requirem ents of a governance system for enterprise inform ation and technology. 
Principles for a governance fram ew ork that can be used to build a governance system  for the enterprise. 
The six principles for a governance system  ( figure 2.1 ) are:
Each enterprise needs a governance system  to satisfy stakeholder needs and to generate value from  the use of 1.
I& T. Value reflects a balance am ong benefits, risk and resources, and enterprises need an actionable strategy and
governance system  to realize this value.
A  governance system  for enterprise I& T is built from  a num ber of com ponents that can be of different types and 2.
that w ork together in a holistic w ay.
A  governance system  should be dynam ic. This m eans that each tim e one or m ore of the design factors are 3.
changed (e.g., a change in strategy or technology), the im pact of these changes on the EGIT system  m ust be
considered. A  dynam ic view  of EGIT leads tow ard a viable and future-proof EGIT system .
A  governance system  should clearly distinguish betw een governance and m anagem ent activities and structures. 4.
A  governance system  should be custom ized to the enterprise’s needs, using a set of design factors as param eters 5.
to custom ize and prioritize the governance system  com ponents.
A  governance system  should cover the enterprise end to end, focusing on not only the IT function but on all 6.
technology and inform ation processing the enterprise puts in place to achieve its goals, regardless of its location
in the enterprise. 7
4
4
7 H uygh, T.; S. D e H aes; “U sing the V iable System  M odel to Study IT Governance D ynam ics: Evidence from  a Single C ase Study,” Proceedings of the
51 st H aw aii International C onference on System  Sciences , 2018, https://scholarspace.m anoa.haw aii.edu/bitstream /1 01 25/50501 /1 /paper061 4.pdf

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

19

# C H A P TE R  2

P O SITIO N IN G E N TE R P R ISE  GO V E R N A N C E  O F  I&T

The three principles for a governance fram ew ork ( figure 2.2 ) are:
A  governance fram ew ork should be based on a conceptual m odel, identifying the key com ponents and 1.
relationships am ong com ponents, to m axim ize consistency and allow  autom ation.
A  governance fram ew ork should be open and flexible. It should allow  the addition of new  content and the ability 2.
to address new  issues in the m ost flexible w ay, w hile m aintaining integrity and consistency.
A  governance fram ew ork should align to relevant m ajor related standards, fram ew orks and regulations. 3.

Figure 2.1 — G overnance System  P rinciples

## 1. Provide

Stakeholder
Value

## 2. Holistic

Approach

## 3. Dynamic

Governance
System

## 4. Governance

## Distinct From

Management

## 5. Tailored to

Enterprise
Needs

## 6. End-to-End

Governance
System
Figure 2.2— G overnance Fram ew ork P rinciples

## 1. Based o n

Conceptual
Model

## 2. Open and

Flexible

## 3. Aligned to

## Maj or Standards

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

20
2.2.2  Governance System  and C om ponents
To satisfy governance and m anagem ent objectives, each enterprise needs to establish, tailor and sustain a governance
system  built from  a num ber of com ponents. Several basic concepts pertaining to governance system s are:
C om ponents can be of different types. The m ost fam iliar are processes, but organizational structures; inform ation 
item s; skills and com petencies; culture and behavior; policies and procedures; and services, infrastructure and
applications are also com ponents of a governance system  and need to be considered.
C om ponents of all types can be generic or can be variants of generic com ponents. 
Generic com ponents are described in the C O B IT core m odel (see C O BIT ® 201 9 Fram ew ork: Introduction and 
M ethodology , Figure 4.2), and apply in principle to any situation. H ow ever, they are generic in nature and
generally need custom ization before being practically im plem ented.
Variants are based on generic com ponents but are tailored for a specific purpose or context w ithin a focus area 
(e.g., for inform ation security, D evO ps, a particular regulation).
2.2.3   Governance and M anagem ent O bjectives
C O B IT includes governance and m anagem ent objectives and underlying processes that help guide the creation and
m aintenance of the governance system  and its different com ponents. In that respect, the tw o key governance and
m anagem ent objectives are:
ED M 01 Ensured governance fram ew ork setting and m aintenance (culture, ethics and behavior; principles, policies 
and fram ew orks; organizational structures; and processes)
A PO 01 M anaged I& T m anagem ent fram ew ork (culture, ethics and behavior; principles, policies and fram ew orks; 
organizational structures; and processes)
C O B IT governance and m anagem ent objectives ensure that enterprises organize their I& T-related activities in a
repeatable and reliable w ay. The C O B IT core m odel— w ith five dom ains, 40 governance and m anagem ent
objectives, and underlying processes that form  the structure for detailed C O B IT guidance— is described and
elaborated in C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

21

# C H A P TE R  3

# T A K IN G TH E  F IR ST STE P S TO W A R D E GIT

## Chapter 3

## Taking the F irst Steps Tow ard E GIT

3.1  C reating the A ppropriate E nvironm ent
It is im portant for the appropriate context to exist w hen im plem enting EGIT im provem ents. This helps ensure that
the initiative is governed and adequately guided and supported by m anagem ent. M ajor I& T initiatives often fail due
to inadequate m anagem ent direction, support and oversight. EGIT im plem entations are no different; they have m ore
chance of success if they are w ell governed and w ell m anaged.
Inadequate support and direction from  key stakeholders can, for exam ple, result in EGIT initiatives that produce new
policies and procedures w ithout proper ow nership or lasting effect. Im provem ents are unlikely to becom e norm al
business practices w ithout a m anagem ent structure that assigns roles and responsibilities, com m its to their continued
operation, and m onitors conform ance.
A n appropriate environm ent should, therefore, be created and m aintained to ensure that EGIT is im plem ented as an
integral part of an overall governance approach w ithin the enterprise. This should include adequate direction and
oversight of the im plem entation initiative, including guiding principles. The objective is to provide sufficient
com m itm ent, direction and control of activities so that there is alignm ent w ith enterprise objectives and appropriate
im plem entation support from  the board and executive m anagem ent.
Experience has show n that, in som e cases, an EGIT initiative identifies significant w eaknesses in overall enterprise
governance. Success of EGIT is m uch m ore difficult w ithin a w eak enterprise governance environm ent, so active
support and participation of senior executives becom e even m ore critical. The board and executives should be aw are
of corporate governance concepts, should understand the need to im prove overall governance, and should
acknow ledge the risk of EGIT failing if w eaknesses are not addressed.
W hether the im plem entation is a sm all or m ajor initiative, executive m anagem ent m ust be involved in, and drive
creation of, the appropriate governance structures. The initial activities usually include assessm ent of current
practices and the design of im proved structures. In som e cases, the initiative can lead to reorganization of the
business as w ell as the IT function and its relationship to business units.
Executive m anagem ent should set and m aintain the governance fram ew ork. This m eans specifying the structures,
processes and practices for EGIT in line w ith agreed governance design principles, decision-m aking m odels,
authority levels and the inform ation required for inform ed decision m aking. 8
1
Executive m anagem ent should also allocate clear roles and responsibilities for directing the EGIT im provem ent
program .
A  com m on approach to form alize EGIT and provide a m echanism  for executive and board oversight and direction of
I& T-related activities is to establish an I& T governance board. 9
2 This I& T governance board acts on behalf of the
board of directors (to w hich it is accountable). The I& T governance board is responsible for how  I& T is used w ithin
the enterprise and for m aking key I& T-related decisions affecting the enterprise. It should have a clearly defined
m andate and is best chaired by a business executive (ideally a board m em ber). It should be staffed by senior business
executives representing the m ajor business units, as w ell as the chief inform ation officer (C IO ), chief digital officer
(C D O ) and/or chief technology officer (C TO ), and, if required, other senior IT m anagers. Internal audit, inform ation
security and risk functions should provide an advisory role.
1
8 See the appendix for an exam ple decision m atrix.
2
9 The I& T governance board m ay also be called an IT steering com m ittee, IT council, IT executive com m ittee or IT governance com m ittee.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

22
Executives need to m ake decisions based on facts; reliable inform ation; and diverse, w ell-founded opinions from
business and IT m anagers, auditors, custom ers, users and others. The C O B IT fram ew ork facilitates these
com m unications by providing a com m on language for executives to express goals, objectives and expected results.
Figures 3.1 and 3.2 illustrate generic roles for key stakeholders and outline responsibilities for im plem enting the
appropriate environm ent to sustain governance and ensure successful outcom es. Sim ilar figures are provided for
each phase of the im plem entation life cycle introduced in the next section.

Figure 3 .1 — R oles in Creating the Appropriate Environm ent
W hen you are... Your role in creating the appropriate environm ent is to...
Board and executives  Set direction for the program 
Ensure alignment with enterprisewide governance and risk management 
Approve key program roles and deﬁne responsibilities 
Give visible support and commitment 
Sponsor, communicate and promote the agreed initiative 
Business management  Provide appropriate stakeholders and champions to drive commitment and support the 
program
Nominate key program roles and deﬁne and assign responsibilities 
IT management  Ensure that the business and executives understand and appreciate the high-level I&T-related 
issues and objectives
Nominate key program roles and deﬁne and assign responsibilities 
Nominate a person to drive the program in agreement with the business 
Internal audit  Agree on the role and reporting arrangements for audit participation 
Ensure an adequate level of audit participation through the duration of the program 
Risk, compliance and
legal
Ensure an adequate level of participation through the duration of the program 
Figure 3 .2— R esponsibilities of Im plem entation R ole P layers

## Key Activities

## Responsibilities of Implementation Role Pla yers

Board

## I&T Governance Board

# CIO

## Business Executive

## IT Managers

## IT Process Owners

## IT Audit

## Risk and Compliance

## Program Steering

Set dir ection for the p r o g r a m .  A  R  R  C  C  I  C  C  C

## Provide program management resources. C A R R C C R R I

Establish and maintain direction and oversight structures and processes. C A C I I I I I R

## Establish and maintain program. I A R C C I I I R

## Align ap proaches with enterprise approaches. I A R C C I C C R

A RACI char t identif ies who is Responsible, Accountable, Cons ulted and/or  Informed.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

23

# C H A P TE R  3

# T A K IN G TH E  F IR ST STE P S TO W A R D E GIT

3.2  A pplying a C ontinual Im provem ent Life C ycle A pproach
The continual im provem ent life cycle approach allow s enterprises to address the com plexity and challenges typically
encountered during EGIT im plem entation. There are three interrelated com ponents to the life cycle, as illustrated in
figure 3.3 :
The core EGIT continual im provem ent life cycle 1.
C hange enablem ent (addressing behavioral and cultural aspects of im plem entation or im provem ent) 2.
Program  m anagem ent 3.
Figure 3.3 depicts the initiatives as continual life cycles to em phasize the fact that they are not isolated,
discontinuous or one-off activities. Instead, they form  an ongoing process of im plem entation and im provem ent that
ultim ately becom es business as usual— at w hich point, the program  can be retired.

Figure 3.4 illustrates the seven phases of the im plem entation road m ap. H igh-level health checks, assessm ents and
audits often trigger consideration of an EGIT initiative, and their results can becom e input to phase 1. A n
im plem entation and im provem ent program  is typically continual and iterative. D uring its last phase, new  objectives
and requirem ents often surface, and a new  cycle m ay begin.
Figure 3 .3 — Applying a Continual Im provem ent Life Cycle Approach
Creation of the appropriate environment
Program management
Change enablement
Continual
impr ovement
lif e cy cle

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

24

3.2.1  P hase 1— W hat A re the Drivers?
Phase 1 identifies current change drivers and creates at executive m anagem ent levels a desire to change that is then
expressed in an outline of a business case. A  change driver is an internal or external event, condition or key issue that
serves as stim ulus for change. Events, trends (industry, m arket or technical), perform ance shortfalls, softw are
im plem entations and even the goals of the enterprise can act as change drivers.
R isk associated w ith im plem entation of the program  itself is described in the business case and m anaged throughout
the life cycle. Preparing, m aintaining and m onitoring a business case are fundam ental and im portant disciplines for
justifying, supporting and then ensuring successful outcom es for any initiative, including the im provem ent of the
governance system . They ensure a continuous focus on the benefits of the program  and their realization.
3.2.2  P hase 2— W here A re W e N ow ?
Phase 2 aligns I& T-related objectives w ith enterprise strategies and risk, and prioritizes the m ost im portant enterprise
goals, alignm ent goals and governance and m anagem ent objectives. The C O BIT ® 201 9 D esign G uide provides
several design factors to help w ith the selection.
B ased on the selected enterprise and alignm ent goals and other design factors, the enterprise m ust identify critical
governance and m anagem ent objectives and underlying processes that are of sufficient capability to ensure
successful outcom es. M anagem ent needs to know  its current capability and w here deficiencies m ay exist. This can
be achieved by a process capability assessm ent of the current status of the selected processes.
Figure 3 .4— CO B IT Im plem entation R oad M ap
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

25

# C H A P TE R  3

# T A K IN G TH E  F IR ST STE P S TO W A R D E GIT

3.2.3   P hase 3 — W here Do W e W ant to B e?
Phase 3 sets a target for im provem ent follow ed by a gap analysis to identify potential solutions.
Som e solutions w ill be quick w ins and others m ore challenging, long-term  tasks. Priority should be given to projects
that are easier to achieve and likely to give the greatest benefit. Longer-term  tasks should be broken dow n into
m anageable pieces.
3.2.4  P hase 4— W hat N eeds to B e Done?
Phase 4 describes how  to plan feasible and practical solutions by defining projects supported by justifiable business
cases and a change plan for im plem entation. A  w ell-developed business case can help ensure that the project’s
benefits are identified and continually m onitored.
3.2.5   P hase 5 — H ow  Do W e Get There?
Phase 5 provides for im plem enting the proposed solutions via day-to-day practices and establishing m easures and
m onitoring system s to ensure that business alignm ent is achieved, and perform ance can be m easured.
Success requires engagem ent, aw areness and com m unication, understanding and com m itm ent of top m anagem ent,
and ow nership by the affected business and IT process ow ners.
3.2.6  P hase 6— Did W e Get There?
Phase 6  focuses on sustainable transition of the im proved governance and m anagem ent practices into norm al
business operations. It further focuses on m onitoring achievem ent of the im provem ents using the perform ance
m etrics and expected benefits.
3.2.7  P hase 7— H ow  Do W e Keep the M om entum  Going?
Phase 7 review s the overall success of the initiative, identifies further governance or m anagem ent requirem ents and
reinforces the need for continual im provem ent. It also prioritizes further opportunities to im prove the governance
system .
Program  and project m anagem ent is based on good practices and provides for checkpoints at each of the seven
phases to ensure that the program ’s perform ance is on track, the business case and risk are updated, and planning for
the next phase is adjusted as appropriate. It is assum ed that the enterprise’s standard approach w ould be follow ed.
Further guidance on program  and project m anagem ent can also be found in C O B IT m anagem ent objectives B A I01
M anaged program s and B A I11 M anaged projects . A lthough reporting is not m entioned explicitly in any of the
phases, it is a continual thread through all of the phases and iterations.
The tim e spent per phase w ill differ greatly depending on the enterprise environm ent, its m aturity, and the scope of
the im plem entation or im provem ent initiative (am ong other factors). H ow ever, the overall tim e spent on each
iteration of the full life cycle ideally should not exceed six m onths, w ith im provem ents applied progressively.
O therw ise, the program  risks losing m om entum , focus and buy-in from  stakeholders. The goal is to establish a
rhythm  of regular im provem ent. Larger-scale initiatives should be structured as m ultiple iterations of the life cycle.
O ver tim e, the life cycle w ill be follow ed iteratively w hile building a sustainable approach. Phases of the life cycle
becom e everyday activities; continual im provem ent occurs naturally and becom es norm al business practice.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

26
3.3   Getting Started— Identify the N eed to A ct: R ecognizing P ain Points and Trigger
E vents
M any factors can indicate a need for new  or revised EGIT practices— and w hen studied closely, they som etim es
reveal com plex netw orks of underlying issues. For exam ple, if the business has the perception that I& T costs are
unacceptably high, this m ay be due to governance and/or m anagem ent issues (e.g., the use of inappropriate criteria in
m anaging IT investm ent). B ut, the pain point m ay be a sym ptom  of long-term , legacy underinvestm ent in I& T that
now  m anifests in significant, new  or ongoing cost.
U sing pain points or trigger events to launch EGIT initiatives m akes it possible to relate the business case for
im provem ent to concrete stakeholder issues, and thereby im prove buy-in. A  sense of urgency w ithin the enterprise
m ay be necessary to kick-start im plem entation. In addition, it can support quick w ins and dem onstrate the addition of
value in areas that are the m ost visible or recognizable in the enterprise. Q uick w ins, in turn, provide a platform  for
introducing further changes and can help consolidate w idespread com m itm ent from  senior m anagem ent, along w ith
support for m ore pervasive im provem ent.
3.3 .1  Typical P ain Points
New  or revised EGIT practices can typically solve— or help to address— the follow ing sym ptom s, w hich w ere also
listed in the C O BIT ® 201 9 D esign G uide under D esign Factor 4 I& T-related issues . (Please note that this list is not
exhaustive, and that each organization has their ow n issues to address.)
Frustration betw een different IT entities across the organization because of a perception of low  contribution 
to business value — M ore and m ore enterprises have decentralized or decoupled IT entities; each provides specific
(and often discontinuous) services to its stakeholders. D ependencies m ay persist am ong the groups; w hen
dependencies are not carefully m anaged, they m ay com prom ise IT effectiveness and efficiency.
Frustration betw een business departm ents (i.e., the IT custom er) and the IT departm ent because of failed 
initiatives or a perception of low  contribution to business value — W hile m any enterprises continue to increase
their investm ents in I& T, the value of these investm ents and overall perform ance of IT are often questioned and/or
not fully understood. This frustration can indicate an EGIT issue, and suggests im proving com m unication betw een
IT and the business, and/or establishing a com m on view  on the role and value of IT. It can also be a consequence
of suboptim al portfolio and project form ulation, proposal and approval m echanism s.
Significant I& T-related incidents, such as data loss, security breaches, project failure, application errors, 
linked to IT — Significant incidents (including data loss, security breaches, project failure and application errors
linked to IT) are often the tip of the iceberg and their im pact can be exacerbated if they receive public and/or m edia
attention. Further investigation often leads to the identification of deeper, structural m isalignm ents— or even the
com plete lack of an IT risk-aw are culture w ithin the enterprise. Stronger EGIT practices are typically required to
understand and m anage IT-related risk com prehensively.
Service delivery problem s by the IT outsourcer(s) — Issues w ith service delivery from  external service 
providers (e.g., consistent failure to m eet agreed service levels) m ay be due to governance issues. For exam ple,
defined third-party service m anagem ent processes m ay be lacking or inadequately tailored (including control and
m onitoring), and/or lack proper responsibilities and accountabilities to fulfill business and IT-service requirem ents.
Failure to m eet IT-related regulatory or contractual requirem ents — In m any enterprises, ineffective or 
inefficient governance m echanism s prevent com plete integration of relevant law s, regulations and contractual
term s into organizational system s. A lternatively, law s, regulations and contractual term s m ay be integrated, but the
enterprise still lacks an approach for m anaging them . (R egulations and com pliance requirem ents continue to
proliferate globally, and often affect IT-enabled activities directly.)

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

27

# C H A P TE R  3

# T A K IN G TH E  F IR ST STE P S TO W A R D E GIT

Regular audit findings or other assessm ent reports about poor IT perform ance or reported IT quality or 
service problem s — Poor assessm ents m ay indicate that service levels are not in place or not functioning w ell, or
that the business is not adequately involved in IT decision m aking.
Substantial hidden and rogue IT spending — Excessive spending outside of norm al IT investm ent decision 
m echanism s and approved budgets often indicates a lack of sufficiently transparent and com prehensive control
over IT expenditures and investm ents. IT spending can be hidden or m isclassified in business-unit budgets,
creating an overall biased view  of IT costs.
Duplications or overlaps betw een various initiatives, or other form s of w asted resources — D uplicative 
projects and/or redundant deploym ent of resources m ay result w hen I& T initiatives are not fully represented in a
single, com prehensive view  of the portfolio. Process and decision-structure capabilities around portfolio and
perform ance m anagem ent m ay not be in place.
Insufficient IT resources, staff w ith inadequate skills and staff burnout/dissatisfaction — These are significant 
IT hum an resource m anagem ent issues that require effective oversight and good governance to address people
m anagem ent and skills developm ent effectively. They m ay also indicate underlying w eaknesses in IT-dem and
m anagem ent and internal service-delivery practices (am ong other latent issues).
IT-enabled changes or projects frequently failing to m eet business needs and delivered late or over budget —
These pain points could relate to problem s w ith business-IT alignm ent, poor definition of business requirem ents,
lack of a benefit-realization process, suboptim al im plem entation or issues in project/program  m anagem ent
processes.
Multiple and com plex IT assurance efforts — This scenario could indicate poor coordination betw een the 
business and IT regarding the need for, and execution of, IT-related assurance review s. A  low  level of business
trust in IT m ay prom pt the business to initiate its ow n review s. A lternatively, it could suggest a lack of business
accountability for, or involvem ent in, IT-assurance review s, if the business is sim ply not aw are w hen review s take
place.
Reluctance of board m em bers, executives or senior m anagem ent to engage w ith IT, or lack of com m itted 
business sponsors for IT — These pain points often indicate a lack of business understanding and insight into IT,
insufficient IT visibility at appropriate levels, or ineffective m anagem ent structures. The pain points m ay also
indicate issues w ith board m andates, w hich are often caused by poor com m unication betw een the business and IT,
and/or m isunderstanding of the business and IT by the business sponsors for I& T.
Com plex IT operating m odel and/or unclear decision m echanism s for IT-related decisions — D ecentralized or 
federated IT organizations often have different structures, practices and policies. The resulting com plexity requires
a strong focus on EGIT to ensure optim al IT decision m aking, and effective and efficient operations. This pain
point often becom es m ore significant w ith globalization: each territory or region m ay have specific (and
potentially unique) internal and external environm ental factors to be addressed.
Excessively high cost of IT — IT is often perceived as a cost to the organization— a cost that should be kept as low 
as possible. This issue typically occurs w hen IT budgets are spent prim arily on projects that bring little value to the
business, keeping the lights on, instead of bringing new  opportunities and innovation. Lack of a holistic, portfolio
view  of all I& T initiatives can contribute to excess cost and m ay indicate that process and decision-structure
capabilities around portfolio and perform ance m anagem ent are not in place.
Obstructed or failed im plem entation of new  initiatives or innovations caused by the current IT architecture 
and system s — In m any organizations, legacy IT architecture does not allow  m uch flexibility in the
im plem entation of new , innovative solutions. D igitization often requires fast action and agile responses to
changing circum stances. It requires a new , m ore flexible approach to IT developm ent and operations, and therefore
directly im plicates the governance system .
Gap betw een business and technical know ledge — B usiness users and IT specialists often speak different 
languages. W hen business users lack sufficient understanding of I& T, or fail to grasp how  I& T can im prove the
business— or conversely, w hen IT specialists m isconstrue challenges and opportunities in the business context—
the enterprise cannot grow  and innovate as it should to be successful. This situation requires good governance to
ensure that people m anagem ent and skills developm ent are addressed effectively.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

28
Regular issues w ith data quality and integration of data across various sources — Enterprises increasingly 
realize the potential value that m ay be hidden in their inform ation. A ll issues of data quality or data integration can
have a substantial im pact on the success of the enterprise. EGIT is key to establishing the right processes, roles,
responsibilities, culture, etc., to deliver business value from  inform ation.
High level of end-user com puting, creating (am ong other issues) a lack of oversight and quality control over 
the applications that are being developed and put in operation — A  high level of end-user com puting m ay strain
com m unication betw een IT and the business, and could entail loose controls around installation of business
applications. It m ay result from  suboptim al portfolio and project form ulation, and/or inadequate proposal and
approval m echanism s. EGIT can help establish a com m on view  on the role and value of IT to optim ize security
and functionality of end-user devices.
Business departm ents im plem enting their ow n inform ation solutions w ith little or no involvem ent of the 
enterprise IT departm ent — This pain point m ay relate to the end-user com puting issue and the optim al use of
data and inform ation; how ever, it prim arily results w hen the business attem pts to im plem ent m ore robust solutions
and services in the norm al course of pursuing business advantage. Lack of com m unication or trust betw een
business and IT can contribute to unsanctioned, independent developm ent, or exacerbate its sym ptom s (in the form
of service issues, etc.).
Ignorance of and/or noncom pliance w ith security and privacy regulations — M itigating new  security and 
privacy threats should be on the agenda of every enterprise, not only for com pliance reasons but also to preserve
the value the enterprise generates. Ignorance and/or noncom pliance w ith regulations can seriously im pair the
enterprise and should be m anaged through proper EGIT.
Inability to exploit new  technologies or innovate using I& T — A  com m on business com plaint casts IT in a 
supporting role, w hereas the enterprise needs IT to innovate and provide a com petitive edge. Such com plaints m ay
point to a lack of true bidirectional alignm ent betw een business and IT, w hich could reflect com m unication issues
or a need to increase business involvem ent in IT decision m aking. A lternatively, the business m ay involve IT too
late in its strategic planning or business initiatives. The issue often  arises m ost em phatically w hen econom ic
conditions require rapid enterprise responses, such as the introduction of new  products or services.
3.3 .2  Trigger E vents in the Internal and E xternal E nvironm ents
In addition to the paint points described in Section 3.3.1, other events in the enterprise’s internal and external
environm ents can signal or trigger a focus on EGIT and drive it high on the enterprise agenda.
Merger, acquisition or divestiture — These transactions m ay result in significant strategic and operational 
consequences relating to I& T. D ue diligence review s m ust gain an understanding of IT issues in the
environm ent(s). Integration or restructuring requirem ents m ay prescribe EGIT m echanism s appropriate for the new
environm ent.
Shifts in the m arket, econom y or com petitive position — A n econom ic dow nturn could lead enterprises to revise 
EGIT m echanism s to facilitate large-scale cost optim ization or perform ance im provem ent.
Changes in business operating m odel or sourcing arrangem ents — M oving from  a decentralized or federated 
m odel to a m ore centralized operating m odel w ill require changes to EGIT practices to enable m ore centralized IT
decision m aking. Im plem entation of shared service centers for areas like finance, hum an resources (H R ) or
procurem ent can also require increased EGIT. Fragm ented IT application or infrastructure dom ains m ay be
consolidated, w ith associated changes in the IT decision-m aking structures or processes that govern them . The
outsourcing of som e IT functions and business processes m ay sim ilarly lead to a renew ed focus on EGIT. A  change
in risk appetite can influence EGIT arrangem ents, if, for exam ple, an enterprise decides to accept m ore risk in
pursuing its objectives.
New  regulatory or com pliance requirem ents — C om plying w ith law s and regulations often has EGIT 
ram ifications. For exam ple, expanded corporate governance reporting requirem ents and financial regulations often
trigger a need for better EGIT as w ell as a focus on inform ation privacy, given the pervasiveness of IT.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

29

# C H A P TE R  3

# T A K IN G TH E  F IR ST STE P S TO W A R D E GIT

Significant technology change or paradigm  shifts — Som e enterprises have m igrated to a service-oriented 
architecture (SO A ) and cloud com puting. These kinds of initiatives fundam entally change the w ay that
infrastructure and application functionality are developed and delivered, and m ay require changes in the
governance and m anagem ent of associated processes and other com ponents.
Enterprisew ide governance focus or project — Large-scale projects, including, for exam ple, broad changes in 
com pany policies, are likely to trigger initiatives in the EGIT area.
New  leadership — The appointm ent of new  C -level representatives, including the chief inform ation officer (C IO ), 
chief financial officer (C FO ), chief executive officer (C EO ) or board m em bers, often triggers an assessm ent of
current EGIT m echanism s and initiatives to address any w eak areas.
External audit or consultant assessm ents — A n assessm ent against appropriate practices, perform ed by an 
independent third party, can be the starting point of an EGIT im provem ent initiative.
New  business strategy or priority — Pursuing a new  business strategy often has EGIT im plications. For exam ple, 
a business strategy of being close to custom ers— know ing w ho they are, understanding their requirem ents and
responding in the best possible m anner— m ay require m ore freedom  of IT decision m aking (for a given business
unit or country), as opposed to centralized decision m aking at the corporate or holding-com pany level.
Desire to significantly im prove the value gained from  I& T — A  need to im prove com petitive advantage, 
innovate, optim ize assets or create new  business opportunities can call attention to EGIT.
These triggers have a direct link to the design factors that are explained in detail in the C O BIT ® 201 9 D esign
G uide . The enterprise builds and tailors its governance system  based on a num ber of design factors. C hanges in
those design factors trigger a review  of EGIT. For exam ple, enterprise strategy is an im portant design factor and
correlates directly to trigger events such as acquisitions, shifts in the m arket or a new  business strategy. A nother
im portant design factor is the level of com pliance requirem ents to w hich the enterprise is subject, w hich directly
links to trigger events such as new  regulatory or com pliance requirem ents.
The identification of pain points and internal or external trigger events leads to recognition, solicitation and
com m unication of the need to act. This com m unication can take the form  of a w ake-up call (w hen pain points are
experienced), or express the im provem ent opportunity and benefits that m ay be realized. C urrent EGIT pain points or
trigger events provide starting points. They can typically be identified through high-level health checks, diagnostics
or capability assessm ents. These techniques have the added benefit of creating consensus on the issues to be
addressed. It can be beneficial to obtain a third party’s independent and objective high-level review  of the current
situation (w hich m ay increase buy-in to act).
It is critical to strive for com m itm ent and buy-in from  the board and executive m anagem ent from  the beginning. To
do this, the EGIT program  and its objectives and benefits need to be clearly expressed in business term s. The correct
level of urgency m ust be instilled. The board and executive m anagem ent should be m ade aw are of the value that
w ell-governed and -m anaged I& T can bring to the enterprise and the risk of not taking action. Engagem ent of the
board and senior m anagem ent also supports up-front consideration of alignm ent am ong the EGIT program ,
enterprise objectives and strategy, enterprise objectives for IT, enterprise governance, and ER M  initiatives (if
existing). Identifying and realizing som e quick w ins (visible issues that can be addressed relatively quickly, and help
establish credibility of the overall initiative by dem onstrating benefits) can be a useful m echanism  for obtaining
board com m itm ent.
O nce the direction has been set at the top, an overall view  of change enablem ent at all levels should be established.
The w ider scale and scope of change m ust be understood first in hard business term s, but the hum an and behavioral
perspective cannot be overlooked. A ll stakeholders involved in, or affected by, the change need to be identified, and
their position relative to the change should be established.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

30
3.3 .3   Stakeholder Involvem ent
M any stakeholders need to collaborate to achieve the overall objective of im proved IT perform ance. The approach
provided in this guide w ill help to develop an agreed and com m on understanding of w hat needs to be achieved to
satisfy specific stakeholder concerns in a coordinated and harm onized w ay. The m ost im portant stakeholders and
their concerns are:
Board and executive m anagem ent — H ow  do w e set and define enterprise direction for the use of I& T and 
m onitor the establishm ent of relevant and required EGIT com ponents, so that business value is delivered, and IT-
related risk is m itigated?
Senior business m anagem ent, IT m anagem ent 10
3 and process ow ners — H ow  do w e enable the enterprise to 
define alignm ent goals to ensure that business value is delivered from  the use of I& T and that IT-related risk is
m itigated?
Business m anagem ent, IT m anagem ent and process ow ners — H ow  do w e plan, build, deliver and m onitor 
inform ation and IT solutions and service capabilities as required by the business and directed by the board?
Risk, com pliance and legal experts — H ow  do w e ensure that the enterprise com plies w ith policies, regulations, 
law s and contracts, and that risk is identified, assessed and m itigated?
Internal audit — H ow  do w e provide independent assurance on value delivery and risk m itigation? 
K ey success factors for im plem entation are:
B oard provides direction, and executive m anagem ent provides the m andate and resources. 
A ll parties understand the enterprise and I& T-related objectives. 
Effective com m unication and enablem ent of the necessary organizational and process changes exist. 
Fram ew orks and good practices are tailored to fit the purpose and design of the enterprise. 
The initial focus is on quick w ins and the prioritization of the m ost beneficial im provem ents that are easiest to 
im plem ent. This dem onstrates benefits and builds confidence for further im provem ent.
3.4  R ecognizing Stakeholders’ R oles and R equirem ents
3.4.1  Internal Stakeholders
Figure 3.5 provides an overview  of internal stakeholders, their m ost im portant high-level responsibilities and
accountabilities in the im provem ent process, and their interest in the outcom es of the im plem entation program . The
follow ing stakeholders represent generic exam ples; som e adaptation, extension and custom ization w ill be required.

3
10 IT m anagem ent includes all roles w ithin the IT function at a m anagem ent level.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

31

# C H A P TE R  3

# T A K IN G TH E  F IR ST STE P S TO W A R D E GIT

## Figure 3 .5— O verview  of Internal EG IT Stakeholders

## Internal Stakeholders Im portant H igh-Level Accountabilities and

Responsibilities

## Interest in the Im plem entation Program

O utcom es
Board and executive
management
Set the overall direction, context and objectives
for the improvement program and ensure
alignment with the enterprise business strategy,
governance and risk management. Provide
visible support and commitment for the
initiative, including the roles of sponsoring and
promoting the initiative. Approve the outcomes
of the program, and ensure that envisioned
beneﬁts are attained and corrective measures
are taken as appropriate. Ensure that the
required resources (ﬁnancial, human and other)
are available to the initiative. Set the direction at
the top and lead by example.
The board and executive management are
interested in obtaining the maximum business
beneﬁts from the implementation program.
They want to ensure that all relevant, required
issues and areas are addressed; required
activities are undertaken; and expected
outcomes are successfully delivered.
Business management
and business process
owners
Provide applicable business resources to the
core implementation team. Work with IT to
ensure that the outcomes of the improvement
program are aligned to and appropriate for the
business environment of the enterprise, value is
delivered, and risk is managed. Visibly support
the improvement program and work with IT to
address any issues that are experienced. Ensure
that the business is adequately involved during
implementation and in the transition to use.
These stakeholders would like the program to
result in better alignment of I&T with the overall
business environment and their speciﬁc areas.
Chief information
oﬃcer (CIO)
Provide leadership to the program and
applicable IT resources to the core
implementation team. Work with business
management and executives to set the
appropriate objectives, direction and approach
for the program.
The CIO wants to ensure that all EGIT
implementation objectives are attained. For the
CIO, the program should result in mechanisms
that will continually improve the relationship
with, and alignment to, the business (including
having a shared view on I&T performance); lead
to better management of IT supply and demand;
and improve the management of I&T-related
business risk.

## IT management and IT

process owners (such

## as the head of

operations, chief
architect, IT security
manager, privacy
oﬃcer, business
continuity
management
specialist)
Provide leadership for applicable work streams

## of the program and resources to the

implementation team. Give key input into the
assessment of current performance and setting
of improvement targets for process areas with
the respective domains. Provide input on
relevant good practices that should be
incorporated and related expert advice. Ensure
that the business case and program plan are
realistic and achievable.
These stakeholders are interested in ensuring
that the improvement initiative results in better
governance of I&T overall and in their individual
areas, and the business inputs required to do so
are obtained in the best possible way.
Compliance, risk
management and legal
experts
Participate as required throughout the program
and provide compliance, risk management and
legal inputs on relevant issues. Ensure
alignment with the overall ERM approach and
conﬁrm that relevant compliance and risk
management objectives are met, issues are
considered and beneﬁts are attained. Provide
guidance as required during implementation.
These stakeholders want to ensure that the
initiative establishes or improves the
mechanisms for ensuring legal and contract
compliance and effective I&T-related business
risk management, and alignment of these
mechanisms to any enterprisewide approaches
that may exist.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

32
3.4.2  E xternal Stakeholders
In addition to the internal stakeholders listed in figure 3.5 , there are also several external stakeholders. W hile these
stakeholders do not have any direct accountabilities or responsibilities in the im provem ent program , they m ay have
requirem ents that need to be satisfied. Figure 3.6 presents generic exam ples.

## Figure 3 .6— O verview  of External EG IT Stakeholders

External Stakeholders Interest in the Im plem entation Program  O utcom es
Customers and society Organizations exist to serve customers. Thus, customers are directly affected by the degree to
which an enterprise’s EGIT objectives are met. If an enterprise is exposed in the security and
privacy domain, such as through loss of customer banking data, the customer will be affected,
and thus has an interest in the successful outcomes of the EGIT implementation program.
IT service providers Enterprise management should ensure that there is alignment and interface between the
enterprise’s own overall EGIT and the governance and management of the services provided by IT
service providers.
Regulators Regulators are interested in whether the implementation program outcomes satisfy and/or
provide structures and mechanisms to satisfy all applicable regulatory and compliance
requirements.
Shareholders (where
relevant)
Shareholders may partially base investment decisions on the state of an enterprise’s corporate
and EGIT governance and its record of accomplishment in this area.
Figure 3 .5— O verview  of Internal EG IT Stakeholders (cont.)

## Internal Stakeholders Im portant H igh-Level Accountabilities and

Responsibilities

## Interest in the Im plem entation Program

O utcom es
Internal audit Participate as required throughout the program
and provide audit inputs on relevant issues.
Provide advice on current issues being
experienced and input on control practices and
approaches. Review the feasibility of business
cases and implementation plans. Provide advice
and guidance as required during
implementation.
Potentially verify assessment results
independently.
These stakeholders are interested in the
outcomes of the implementation program
related to control practices and approaches, and
how the mechanisms that are established or
improved will enable current audit ﬁndings to be
addressed.
Implementation team
(combined business
and IT team, consisting
of individuals from
previously listed
stakeholder categories)
Direct, design, control, drive and execute the
end-to-end program from the identiﬁcation of
objectives and requirements to the eventual
evaluation of the program against business
case objectives and the identiﬁcation of new
triggers and objectives for further
implementation or improvement cycles. Ensure
skills transfer during the transition from the
implementation environment to the operation,
use and maintenance environments.
The team wants to ensure that all envisioned
outcomes of the EGIT initiative are obtained and
maximized.
Users Support EGIT by performing speciﬁc roles and
responsibilities as assigned to them.
These stakeholders are interested in the
impact(s) the initiative will have on their day-to-
day lives—their jobs, roles and responsibilities,
and activities.
Customers Customers are part of the extended value chain
and have expectations regarding delivery of
services, products, etc.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

33

# C H A P TE R  3

# T A K IN G TH E  F IR ST STE P S TO W A R D E GIT

3.4.3   Independent A ssurance and the R ole of A uditors
IT m anagers and stakeholders need to be aw are of the role of assurance professionals. A ssurance professionals can
be internal auditors, external auditors, International O rganization for Standardization/International Electrotechnical
C om m ission (ISO /IEC ) standards auditors, or any professionals com m issioned to provide an assessm ent on IT
services and processes. It is im portant to take these stakeholders and their interests into account w hen defining the
EGIT im plem entation plan. Increasingly, boards and executive m anagem ent seek independent advice and opinions
regarding critical I& T functions and services. There is also a general increase in the need to dem onstrate com pliance
w ith national and international regulations.
Figure 3 .6— O verview  of External EG IT Stakeholders (cont.)
External Stakeholders Interest in the Im plem entation Program  O utcom es
External auditors External auditors may be able to rely on I&T-related controls more fully as a result of an effective
implementation program, as substantiated by an audit. They are also interested in regulatory
compliance aspects and ﬁnancial reporting.
Business partners (e.g.,
suppliers)
Business partners that use automated electronic transactions with the enterprise could have an
interest in the outcomes of the implementation program with respect to improved information
security, integrity and timeliness. They may also be interested in regulatory compliance and
international standards certiﬁcations that could be outcomes of the program.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

P age intentionally left blank
34

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

35

# C H A P TE R  4

IDE N TIF Y IN G C H A LLE N GE S A N D SU C C E SS F A C TO R S
C hapter 4
Identifying C hallenges and S uccess F actors
4.1  Introduction
Experiences from  EGIT im plem entations have show n that several practical issues need to be overcom e for the
initiative to be successful and for continual im provem ent to be sustained. This chapter describes several of these
challenges, their likely root causes and the factors that should be considered to ensure successful outcom es.
4.2  C reating the A ppropriate E nvironm ent
4.2.1  P hase 1— W hat A re the Drivers?
Figure 4.1 lists challenges, their root causes and success factors for phase 1.

Figure 4.1 — Challenges, R oot Causes and Success Factors for P hase 1
Phase 1 — W hat Are the Drivers?
Challenges  Lack of senior management buy-in, commitment and support 
Diﬃculty in demonstrating value and beneﬁts 
Root causes  Lack of understanding (and evidence) of the importance, urgency and value of improved 
governance to the enterprise
Lack of resources 
Poor understanding of the scope of EGIT and the differences between governance and 
management of I&T
Implementation driven by a short-term reaction to a problem rather than a proactive, broader 
justiﬁcation for improvement
Concern about “another project likely to fail”; lack of trust in IT management 
Poor communication of governance issues and beneﬁts; beneﬁts and time frames not clearly 
articulated
No senior executive willing to sponsor or be accountable 
Poor perception of the credibility of the IT function; CIO does not command enough respect 
Executive management’s belief that EGIT is the responsibility of IT management only 
Not having the appropriate team (role players) responsible for EGIT or adequate skills to 
undertake the task
Lack of use of recognized frameworks/lack of training and awareness 
Incorrect positioning of EGIT in the context of current enterprise governance 
Initiative driven by enthusiastic “converts” who preach textbook approaches 
Success factors  Make EGIT a board, audit committee and risk committee agenda item for discussion. 
Create a committee or leverage an existing committee, such as the I&T governance board, to 
provide a mandate and accountability for action.
Avoid making EGIT appear to be a solution looking for a problem. There must be a real need and 
potential beneﬁt.
Identify leader(s) and sponsor(s) with the authority, understanding and credibility to take 
ownership of implementation success.
Identify and communicate pain points that can motivate a desire to change the status quo. 
Use language, approaches and communications appropriate to the audience. Avoid jargon and 
terms the audience members cannot recognize.
Jointly (with the business) deﬁne and agree on expected value from IT. 
Express beneﬁts in (agreed) business terms/metrics. 
Obtain support from, and augment skills with, external auditors, consultants and advisors, if 
required.
Develop guiding principles that set the tone and scene for the transformation effort. 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

36
Figure 4.1 — Challenges, R oot Causes and Success Factors for P hase 1 (cont.)
Phase 1 — W hat Are the Drivers?
Produce imperatives based on the transformation effort particular to the enterprise, building in 
the trust and partnership necessary for success.
Produce a business case tailored for a targeted audience that demonstrates the business 
beneﬁts of the proposed IT investment.
Prioritize and align the business case based on the strategic focus and current enterprise pain 
points.
Align the business case with overall enterprise governance objectives. 
Gain education and training in EGIT issues and frameworks. 
Challenges  Diﬃculty in getting the required business participation 
Diﬃculty in identifying stakeholders and role players 
Root causes  EGIT not a priority for business executives (not a key performance indicator [KPI]) 
IT management’s preference to work in isolation (proving the concept before involving the 
customer)
Barriers between IT and the business, inhibiting participation 
No clear roles and responsibilities for business involvement 
Key business individuals and inﬂuencers not involved or engaged 
Business executives’ and process owners’ limited understanding of the beneﬁts and value of 

# EGIT

Success factors  Encourage top management and the I&T governance board to set mandates and insist on 
business roles and responsibilities in EGIT.
Put in place a process for engaging stakeholders. 
Explain and sell business beneﬁts clearly. 
Explain the risk of noninvolvement. 
Identify critical services or major IT initiatives to use as pilots/models for business involvement 
in improved EGIT.
Find the believers (business users who recognize the value of better EGIT). 
Promote free thinking and empowerment, but only within well-deﬁned polices and a governance 
structure.
Ensure that those who are responsible for and need to drive change are the ones to gain 
sponsor support.
Create forums for business participation—for example, the I&T governance board—and run 
workshops to openly discuss current problems and opportunities for improvement.
Involve business representatives in high-level current-state assessments. 
Challenge  Lack of business insight among IT management 
Root causes  Poor corporate governance performance 
IT leadership with an operational technical background—not involved enough in enterprise 
business issues
IT management isolated within the enterprise—not involved at senior levels 
Weak business relationship process 
Legacy of perceived poor performance that has driven IT and the CIO into a defensive mode of 
operation
CIO and IT management in a vulnerable position, unwilling to reveal internal weaknesses 
Success factors  Enhance credibility by building on successes and performance of respected IT staff. 
Make IT management a permanent member of the enterprise executive committee (if possible),
to ensure that IT management has adequate business insight and is involved early in new
initiatives.
Implement an effective business relationship process. 
Invite business participation and involvement. Consider placing business people in IT and vice 
versa to gain experience and improve communications.
If necessary, reorganize IT management roles and implement formal links to other business 
functions, such as ﬁnance and HR.
Ensure that the CIO has business experience. Consider appointment of a CIO from the business. 
Use consultants to create a stronger business-oriented EGIT strategy. 
Create governance mechanisms, such as business relationship managers within IT, to enable 
greater business insight.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

37

# C H A P TE R  4

IDE N TIF Y IN G C H A LLE N GE S A N D SU C C E SS F A C TO R S
4.2.2  P hase 2— W here A re W e N ow ?  and P hase 3 — W here Do W e W ant to B e?
Figure 4.2 lists the challenges, their root causes and success factors for phases 2 and 3.

Figure 4.2— Challenges, R oot Causes and Success Factors for P hases 2 and 3
Phase 2— W here Are W e N ow ?
Phase 3 — W here Do W e W ant to B e?
Challenges  Inability to gain and sustain support for improvement objectives 
Communication gap between IT and the business 
Root causes  Compelling reasons to act not clearly articulated or nonexistent 
Failure of perceived beneﬁts to suﬃciently justify required investment (cost) 
Concern about loss of productivity or eﬃciency due to change 
Lack of clear accountabilities for sponsoring and committing to improvement objectives 
Lack of appropriate structures with business involvement from strategy to tactical and operational levels 
Inappropriate way of communicating (not suﬃciently simple, not suﬃciently brief, not conveyed in 
business language, not suited to politics and culture) or not adapting style to different audiences
Business case for improvements not well developed or articulated 
Insuﬃcient focus on change enablement and obtaining buy-in at all required levels 
Success factors  Develop agreed understanding of the value of improved EGIT. 
Have the appropriate structures, such as an IT steering committee and an audit committee, facilitate 
communication and agreement of objectives and establish meeting schedules to exchange strategy
status, clarify misunderstandings and share information.
Implement an effective business-relationship process. 
Develop and execute a change enablement strategy and communication plan explaining the need to 
reach a higher level of maturity.
Use the correct language and common terminology with a style adapted to audience subgroups. 
Make it interesting, use visuals.
Develop the initial EGIT business case into a detailed business case for speciﬁc improvements, with clear 
articulation of risk. Focus on added value for the business (expressed in business terms) as well as costs.
Educate and train in COBIT and this implementation method. 
Challenge  Cost of improvements outweighing perceived beneﬁts 
Root causes  Tendency to focus solely on controls and performance improvements, not on eﬃciency 
improvements and innovation
Improvement program inadequately phased and failing to clearly associate improvement beneﬁts 
and cost
Prioritization of complex, expensive solutions rather than lower-cost, easier solutions 
Signiﬁcant IT budget and workforce already committed to maintenance of existing infrastructure,
resulting in a limited appetite to direct funds or staff time left to deal with EGIT
Figure 4.1 — Challenges, R oot Causes and Success Factors for P hase 1 (cont.)
Phase 1 — W hat Are the Drivers?
Challenges  Lack of current enterprise policy and direction 
Weak current enterprise governance 
Root causes  Commitment and leadership issues, possibly due to organizational immaturity 
Autocratic leadership based on individual commands rather than on enterprise policy 
Culture’s promotion of free thinking and informal approaches rather than a control environment 
Weak enterprise risk management 
Success factors  Raise issues and concerns with board-level executives and nonexecutives about the risk of poor 
governance, based on real issues related to compliance and enterprise performance.
Raise issues with the audit committee or internal audit. 
Obtain input and guidance from external auditors. 
Consider how the culture might need to be changed to enable improved governance practices. 
Raise the issue with the CEO and board of directors. 
Ensure that risk management is applied across the enterprise. 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

38
4.2.3   P hase 4— W hat N eeds to B e Done?
Figure 4.3 lists the challenges, their root causes and success factors for phase 4.

Figure 4.2— Challenges, R oot Causes and Success Factors for P hases 2 and 3 (cont.)
Phase 2— W here Are W e N ow ?
Phase 3 — W here Do W e W ant to B e?
Success factors  Identify areas in infrastructure, processes and HR—such as standardization, higher maturity levels and 
fewer incidents—where eﬃciencies and direct cost savings can be made by better governance.
Prioritize based on beneﬁt and ease of implementation, especially quick wins. 
Challenge  Lack of trust and good relationships between IT and the enterprise 
Root causes  Legacy issues underpinned by poor IT track record on project and service delivery 
Lack of IT understanding of business issues and vice versa 
Scope and expectations not properly articulated and managed 
Unclear governance roles, responsibilities and accountabilities in business, causing abdication of key 
decisions
Lack of supporting information and metrics illustrating the need to improve 
Reluctance to be proven wrong, general resistance to change 
Success factors  Foster open and transparent communication about performance, with links to corporate performance 
management.
Focus on business interfaces and service mentality. 
Publish positive outcomes and lessons learned to help establish and maintain credibility. 
Ensure that the CIO has credibility and leadership in building trust and relations. 
Formalize governance roles and responsibilities in the business so that accountability for decisions is 
clear.
Identify and communicate evidence of real issues, risk that needs to be avoided and beneﬁts to be 
gained (in business terms), relating to proposed improvements.
Focus on change enablement planning. 
Figure 4.3 — Challenges, R oot Causes and Success Factors for P hase 4
Phase 4— W hat N eeds to B e Done?
Challenge  Failure to understand the environment 
Root causes  Insuﬃcient consideration of changes needed in the organization and its culture, as well as 
stakeholder perceptions
Insuﬃcient consideration of existing governance strengths and practices within IT and the wider 
enterprise
Success factors  Perform a stakeholder assessment and focus on developing a change enablement plan. 
Build on and use existing strengths and good practices within IT and the wider enterprise. Avoid 
reinventing wheels just for IT.
Understand the different constituencies, their objectives and mindsets. 
Challenge  Various levels of complexity (technical, organizational, operating model) 
Root causes  Poor understanding of EGIT practices 
Attempting to implement too much at once 
Prioritizing critical and diﬃcult improvements with little practical experience 
Complex and/or multiple corporate operating models 
Success factors  Educate and train in COBIT and this implementation method. 
Break down into smaller projects, building a step at a time. Prioritize quick wins. 
Collect the needs for improvement from different constituencies. Correlate and prioritize them and 
map them to the change enablement program.
Focus on business priorities to phase implementation. 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

39

# C H A P TE R  4

IDE N TIF Y IN G C H A LLE N GE S A N D SU C C E SS F A C TO R S
Figure 4.3 — Challenges, R oot Causes and Success Factors for P hase 4 (cont.)
Phase 4— W hat N eeds to B e Done?
Challenge  Diﬃculty in understanding COBIT and associated frameworks, procedures and practices 
Root causes  Inadequate skills and knowledge 
Copying good practices, not adapting them 
Focusing only on procedures, not on other enablers such as roles and responsibilities and skills applied 
Success factors  Educate and train in COBIT, other related standards and good practices, and this implementation method. 
If required, obtain qualiﬁed and experienced external guidance and support. 
Adapt and tailor good practices to suit the enterprise environment. 
When designing processes, consider and deal with required skills, roles and responsibilities, process 
ownership, goals and objectives, and other governance components.
Challenge  Resistance to change 
Root causes  Resistance is a natural behavioral response when the status quo is threatened, but it may also 
indicate underlying concerns such as:
Misunderstanding of what is required and why it is useful
Perception that workload and cost will increase 
Reluctance to admit shortcomings 
Not-invented-here syndrome underpinned by forcing generic governance frameworks onto the 
enterprise
Entrenched thinking, threat to role or power base, not understanding “what’s in it for me” 
Success factors  Focus awareness communications on speciﬁc pain points and drivers. 
Raise awareness by educating business and IT managers and stakeholders. 
Use an experienced change agent with business and IT skills. 
Follow up at regular milestones to ensure that implementation beneﬁts are realized by involved parties. 
Go for quick and relatively easy wins as eye-openers to boost recognition of values provided. 
Make generic frameworks such as COBIT relevant to the context of the enterprise. 
Focus on change enablement planning such as:
Development 
Training 
Coaching 
Mentoring 
Transferring skills 
Organize communication sessions/road shows and ﬁnd champions to promote the beneﬁts. 
Challenge  Failure to adopt improvements 
Root causes  External experts designing solutions in isolation or imposing solutions without adequate explanation 
Internal EGIT team operating in isolation and acting as an informal proxy for real process owners,
causing misunderstandings and resistance to change
Inadequate support and direction from key stakeholders, resulting in EGIT projects producing new 
policies and procedures that have no valid ownership
Success factors  Engage process owners and other stakeholders during design. 
Use pilots and demos, where appropriate, to educate and obtain buy-in and support. 
Start with quick wins, demonstrate beneﬁts and build from there. 
Look for champions who understand resistance, and want to improve, rather than forcing people who 
resist.
Encourage a management structure that assigns roles and responsibilities, commits to their 
continued operation, and monitors compliance.
Enforce knowledge transfer from the external experts to process owners. 
Delegate responsibility and empower the process owners. 
Challenge  Diﬃculty in integrating internal governance approach with the governance models of outsourcing 
partners
Root causes  Fear of revealing inadequate practices 
Failure to deﬁne and/or share EGIT requirements with the outsource provider 
Unclear division of roles and responsibilities 
Differences in approach and expectations 
Contractual arrangements in outsourcing contracts 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

40
4.2.4  P hase 5 — H ow  Do W e Get There?
Figure 4.4 lists the challenges, their root causes and success factors for phase 5.

Figure 4.3 — Challenges, R oot Causes and Success Factors for P hase 4 (cont.)
Phase 4— W hat N eeds to B e Done?
Success factors  Involve suppliers/third parties in implementation and operational activities where appropriate. 
Incorporate conditions and the right to audit in contracts. 
Look for ways to integrate frameworks and approaches. 
Address roles, responsibilities and governance structures with third parties up front, not as an 
afterthought.
Match evidence (via audit and document review) of service provider processes, people and 
technology with required EGIT practices and levels.
Figure 4.4— Challenges, R oot Causes and Success Factors for P hase 5
Phase 5— H ow  Do W e G et There?
Challenge  Failure to realize implementation commitments 
Root causes  Overly optimistic goals, underestimation of effort required 
IT in ﬁre-ﬁghting mode and focused on operational issues 
Lack of dedicated resources or capacity 
Priorities incorrectly allocated 
Scope misaligned with requirements or misinterpreted by implementers 
Program management principles, such as business case, not well applied 
Insuﬃcient insight into business environment (for example, operating model) 
Success factors  Manage expectations. 
Follow guiding principles. 
Keep it simple, realistic and practical. 
Break down the overall project into small, achievable projects. Build experience and beneﬁts. 
Ensure that the implementation scope underpins the requirements and all stakeholders have the 
same understanding of what the scope will deliver.
Focus on implementations that enable business value. 
Ensure that dedicated resources are allocated. 
Apply program management and governance principles. 
Leverage existing mechanisms and ways of working. 
Ensure adequate insight into the business environment. 
Challenge  Trying to do too much at once; tackling overly complex, overly diﬃcult or simply too many problems 
Root causes  Lack of understanding of scope and effort (also for human aspects, lack of common language) 
Not understanding capacity to absorb change (too many other initiatives) 
Lack of formal program planning and management; not building a foundation and maturing the effort 
from there
Undue pressure to implement 
Not capitalizing on quick wins 
Reinventing the wheel and not using what is there as a base 
Lack of insight into organizational landscape 
Lack of skills 
Success factors  Apply program and project management principles. 
Use milestones. 
Prioritize 80/20 tasks (80 percent of the beneﬁt with 20 percent of the effort) and be careful about 
sequencing in the correct order. Capitalize on quick wins.
Build trust/conﬁdence. Have the skills and experience to keep it simple and practical. 
Reuse what is there as a base. 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

41

# C H A P TE R  4

IDE N TIF Y IN G C H A LLE N GE S A N D SU C C E SS F A C TO R S
4.2.5   P hase 6— Did W e Get There?  and P hase 7— H ow  Do W e Keep the M om entum  Going?
Figure 4.5 lists the challenges, root causes and success factors for phases 6  and 7.

Figure 4.5— Challenges, R oot Causes and Success Factors for P hases 6 and 7
Phase 6— Did W e G et There?
Phase 7— H ow  Do W e Keep the M om entum  G oing?
Challenge  Failure to adopt or apply improvements 
Root causes  Solutions too complex or impractical
Solutions developed in isolation by consultants or an expert team 
Good practices copied, but not tailored to suit the enterprise operation 
Solutions not owned by process owners/team 
Organization lacking clear roles and responsibilities 
Management not mandating and supporting change 
Resistance to change 
Poor understanding of how to apply the new processes or tools that have been developed 
Skills and proﬁle not matched with the requirements of the role 
Figure 4.4— Challenges, R oot Causes and Success Factors for P hase 5 (cont.)
Phase 5— H ow  Do W e G et There?
Challenge  IT and/or business in ﬁre-ﬁghting mode 
Root causes  Lack of resources or skills 
Lack of internal processes, internal ineﬃciencies 
Lack of strong IT leadership 
Too many workarounds 
Success factors  Apply good management skills. 
Gain commitment and drive from top management so people are made available to focus on EGIT. 
Address root causes in the operational environment (external intervention, management prioritizing 

# IT).

Apply tighter discipline over and management of business requests. 
Use external resources where appropriate. 
Obtain external assistance. 
Challenge  Lack of required skills and competencies, such as understanding governance, management, business,
processes, soft skills
Root causes  Insuﬃcient understanding of COBIT and IT management good practices 
Business and management skills often not included in training 
IT staff not interested in business areas 
Business staff not interested in IT 
Success factors  Focus on change enablement planning:
Development 
Training 
Coaching 
Mentoring 
Feedback into recruitment process 
Cross-skilling 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

42
Figure 4.5— Challenges, R oot Causes and Success Factors for P hases 6 and 7 (cont.)
Phase 6— Did W e G et There?
Phase 7— H ow  Do W e Keep the M om entum  G oing?
Success factors  Focus on quick wins and manageable projects. 
Make small improvements to test the approach and make sure it works. 
Involve the process owners and other stakeholders in development of the improvement. 
Make sure roles and responsibilities are clear and accepted. Change roles and job descriptions if 
required.
Drive the improvement from management down throughout the enterprise. 
Apply adequate training where required. 
Develop processes before attempting to automate. 
Reorganize to enable better ownership of processes, if required. 
Match roles (especially those that are key for successful adoption) to individual capabilities and 
characteristics.
Provide effective education and training. 
Challenge  Diﬃculty in showing or proving beneﬁts 
Root causes  Goals and metrics not established or working effectively 
Beneﬁts tracking not applied after implementation 
Loss of focus on beneﬁts and value to be gained 
Poor communication of successes 
Success factors  Set clear, measurable and realistic goals (outcome expected from the improvement). 
Set practical performance metrics (to monitor whether the improvement is driving achievement of goals). 
Produce scorecards showing how performance is being measured. 
Communicate, in business impact terms, the results and beneﬁts that are being gained. 
Implement quick wins and deliver solutions in short time scales. 
Challenge  Lost interest and momentum, change fatigue 
Root causes  Continual improvement not part of the culture 
Management not driving sustainable results 
Resources focused on ﬁre-ﬁghting and service delivery, not on improvement 
Personnel not motivated, cannot see the personal beneﬁt in adopting and driving change 
Success factors  Ensure that management regularly communicates and reinforces the need for robust and reliable 
services, solutions and good governance. Communicate to all stakeholders the successful
improvements already achieved.
Revisit stakeholders and get their support to fuel momentum. 
Take opportunities to implement improvements on the job. if resources are scarce, as part of daily 
routine.
Focus on regular and manageable improvement tasks. 
Obtain external assistance, but remain engaged. 
Align personal reward systems with process and organization performance improvement targets 
and metrics.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

43

# C H A P TE R  5

# E N A B LIN G C H A N GE

C hapter 5
Enabling C hange
5.1  The N eed for C hange E nablem ent
Successful im plem entation or im provem ent depends on im plem enting the appropriate change in the correct w ay. In
m any enterprises, there is a significant focus on the first aspect (im plem enting the good practices), but not enough on
the second aspect, im plem enting change in the correct w ay by em phasizing m anagem ent of the hum an, behavioral
and cultural aspects of the change, and m otivating stakeholders to buy into the change. C hange enablem ent, w hich
includes stakeholder m anagem ent, is one of the biggest challenges to EGIT im plem entation.
It should not be assum ed that the various stakeholders involved in, or affected by, new  or revised governance
arrangem ents w ill necessarily readily accept and adopt the change. The possibility of ignorance, resistance to change
or change fatigue needs to be addressed through a structured and proactive approach. 11
1 A lso, optim al aw areness of
the program  should be achieved through a com m unication plan that defines w hat w ill be com m unicated, in w hat
w ay, by w hom  and to w hom , throughout the various phases of the program .
C O B IT defines change enablem ent as a holistic and system atic process of ensuring that relevant stakeholders are
prepared and com m itted to the changes involved in m oving from  a current state to a desired future state.
A ll key stakeholders should be involved. A t a high level, change enablem ent typically entails:
A ssessing the im pact of the change on the enterprise, its people and other stakeholders 
Establishing the future state (vision) in hum an/behavioral term s and the associated m easures that describe it 
B uilding change response plans to m anage change im pacts proactively and m axim ize engagem ent throughout the 
process. These plans m ay include training, com m unication, organization design (job content, organizational
structure), process redesign and updated perform ance m anagem ent system s.
C ontinually m easuring the progress of change tow ard the desired future state 
A lthough every EGIT im plem entation is different, a com m on objective of change enablem ent is having enterprise
stakeholders from  the business and IT lead by exam ple, and encourage staff at all levels to w ork according to the
desired new  w ay. Exam ples of desired behavior include:
Follow ing agreed processes 
Participating in defined EGIT structures such as a change approval or advisory board 
Enforcing defined guiding principles, policies, standards, processes or practices (such as a policy regarding new 
investm ents or security)
This can be best achieved by gaining the com m itm ent of the stakeholders (diligence and due care, leadership, and
com m unicating and responding to the w orkforce) and selling the benefits. If necessary, it m ay be required to enforce
com pliance. In other w ords, hum an, behavioral and cultural barriers m ust be overcom e to establish a com m on
interest in properly adopting the new  w ay, instill the w ill to adopt it and ensure the ability to adopt it. It m ay be
useful to draw  on change enablem ent skills w ithin the enterprise or, if necessary, from  external consultants to
facilitate the change in behavior.
1
11 W hen review ing a m ajor IT transform ation initiative, the U S D epartm ent of Veterans A ffairs (V A ) noted, “The prim ary challenge the V A  w ill face in
achieving this transform ation w ill be gaining the acceptance and support of all V A  personnel, including leadership, m iddle m anagers and field staff.”
See W alters, J.; “Transform ing Inform ation Technology at the D epartm ent of Veterans A ffairs,” IB M  C enter for the B usiness of Governm ent, U SA ,
2009 , http://w w w.isaca.org/K now ledge-C enter/cobit/D ocum ents/W altersVAReport-June09.pdf. The V A  has stated that its effort cannot succeed if it
addresses only technological transform ation; it recognizes that the hum an factor that is needed to achieve acceptance, change the organization and
change the w ay business is conducted is critical to success.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

44
5.1.1  C hange E nablem ent of E GIT Im plem entation
Various approaches to enabling change have been defined over the years, and they provide valuable input that could
be utilized during the im plem entation life cycle. O ne of the m ost w idely accepted approaches to change enablem ent
has been developed by John K otter: 12
2
Establish a sense of urgency. 1.
Form  a pow erful guiding coalition. 2.
C reate a clear vision that is expressed sim ply. 3.
C om m unicate the vision. 4.
Em pow er others to act on the vision. 5.
Plan for and create short-term  w ins. 6.
C onsolidate im provem ents and produce m ore change. 7.
Institutionalize new  approaches. 8.
The K otter approach w as chosen as an exam ple and adapted for the specific requirem ents of an EGIT
im plem entation or im provem ent, as described in this publication. K otter’s adapted precepts are illustrated by the
change enablem ent life cycle in figure 5 .1 .

2
12 K otter, J.; Leading C hange , H arvard B usiness School Press, U SA , 19 9 6 , https://w w w.kotterinc.com /book/leading-change/
Figure 5.1 — Change Enablem ent Life Cycle
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

45

# C H A P TE R  5

# E N A B LIN G C H A N GE

The follow ing subsections create a high-level, but holistic, overview  by discussing briefly each phase of the change
enablem ent life cycle, as applied to a typical EGIT im plem entation.
5.2  P hases in the C hange E nablem ent Life C ycle C reate the A ppropriate
E nvironm ent
The overall enterprise environm ent should be analyzed to determ ine the m ost appropriate change enablem ent
approach. This includes aspects such as the m anagem ent style, culture, form al and inform al relationships, and
attitudes. It is also im portant to understand other I& T or enterprise initiatives that are ongoing or planned, to ensure
that dependencies and im pacts are considered.
It should be ensured from  the start that the required change enablem ent skills, com petencies and experience are
available and utilized. For exam ple, this m ay entail involving resources from  the H R  function or obtaining external
assistance.
A s an outcom e of this phase, the appropriate balance of directive and inclusive change enablem ent activities required
to deliver sustainable benefits can be designed.
5.2.1  P hase 1— E stablish the Desire to C hange
The purpose of this phase is to understand the breadth and depth of the envisioned change, the various stakeholders
that are affected, the nature of the im pact on, and involvem ent required from , each stakeholder group, and the current
readiness and ability to adopt the change.
C urrent pain points and trigger events can provide a good foundation for establishing the desire to change. The w ake-
up call, an initial com m unication on the program , can be related to real-w orld issues the enterprise m ay be
experiencing. A lso, initial benefits can be linked to areas that are highly visible to the enterprise, creating a platform
for further changes and m ore w idespread com m itm ent and buy-in.
W hile com m unication is a com m on thread throughout the im plem entation or im provem ent initiative, the initial
com m unication is one of the m ost im portant, and should dem onstrate the com m itm ent of senior m anagem ent.
Therefore, the initial com m unication should ideally be com m unicated by the executive com m ittee or C EO .
5.2.2  P hase 2— F orm  an E ffective Im plem entation T eam
D im ensions to consider in assem bling an effective core im plem entation team  include involving the appropriate areas
from  business and IT and identifying the know ledge and expertise, experience, credibility, and authority of team
m em bers. O btaining an independent, objective view , as provided by external parties (such as consultants and a
change agent), could also be highly beneficial by aiding the im plem entation process or addressing skill gaps that m ay
exist w ithin the enterprise. Therefore, another dim ension to consider is the appropriate m ix of internal and external
resources.
The essence of the team  should be a com m itm ent to:
A  clear vision of success and desired goals 
Engaging the best in all team  m em bers, all the tim e 
C larity and transparency of team  processes, accountabilities and com m unications 
Integrity, m utual support and com m itm ent to each other’s success 
M utual accountability and collective responsibility 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

46
O ngoing m easurem ent of its ow n perform ance and the w ay it behaves as a team 
Living out of its com fort zone, alw ays looking for w ays to im prove, uncovering new  possibilities and em bracing 
change
It is im portant to identify potential change agents w ithin different parts of the business, w ith w hom  the core team  can
w ork, to support the vision and cascade changes dow n.
5.2.3   P hase 3 — C om m unicate Desired V ision
In this phase, a high-level change enablem ent plan is developed, in conjunction w ith the overall program  plan. A  key
com ponent of the change enablem ent plan is the com m unication strategy, w hich addresses w ho the core audience
groups are, and their behavioral profiles and inform ation requirem ents, com m unication channels, and principles.
The desired vision for the im plem entation or im provem ent program  should be com m unicated in the language of
those affected by it. The com m unication should include the rationale for, and benefits of, the change, the im pacts of
not m aking the change (purpose), the vision (picture), the road m ap to achieving the vision (plan) and the
involvem ent required of the various stakeholders (part). 13
3 Senior m anagem ent should deliver key m essages (such as
the desired vision). The com m unication should note that both behavioral/cultural and logical aspects w ill be
addressed, and the em phasis is on tw o-w ay com m unication. R eactions, suggestions and other feedback should be
captured, and appropriate action taken.
5.2.4  P hase 4— E m pow er R ole P layers and Identify Q uick W ins
A s im provem ents are designed and built, change response plans are developed to em pow er various role players. The
scope of these m ay include:
O rganizational design changes, such as job content or team  structures 
O perational changes, such as process flow s or logistics 
People m anagem ent changes, such as required training and/or changes to perform ance m anagem ent and rew ard 
system s
R ealization of quick w ins is im portant from  a change enablem ent perspective. These could be related to the pain
points and trigger events discussed in C hapter 3. V isible and unam biguous quick w ins can build m om entum  and
credibility for the program  and help to address any skepticism  that m ay exist.
It is im perative to use a participative approach in the design and building of the im provem ents. Engaging those
affected by the change in the actual design— for exam ple, through w orkshops and review  sessions— can increase
buy-in.
5.2.5   P hase 5 — E nable O peration and U se
A s initiatives are im plem ented w ithin the core im plem entation life cycle, the change response plans are also
im plem ented. Q uick w ins that have been realized are built on, and the behavioral and cultural aspects of the broader
transition are addressed (issues such as dealing w ith fears of loss of responsibility, new  expectations and unknow n tasks).
It is im portant to balance group and individual interventions to increase buy-in and engagem ent and to ensure that all
stakeholders obtain a holistic view  of the change.
3
13 R egarding the four Ps (purpose, picture, plan and part), see B ridges, W .; M anaging Transitions: M aking the M ost of C hange , A ddison-W esley, U SA ,
19 9 9 .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

47

# C H A P TE R  5

# E N A B LIN G C H A N GE

D uring the process of solution rollout, m entoring and coaching are critical to ensure uptake in the user environm ent.
The change requirem ents and objectives that had been set during the start of the initiative should be revisited to
ensure that they w ere adequately addressed.
Success m easures should be defined and should include both hard business m easures and perception m easures that
track how  people feel about a change.
5.2.6  P hase 6— E m bed N ew  A pproaches
A s concrete results are achieved, new  w ays of w orking should becom e part of the enterprise’s culture and be rooted
in its norm s and values (“the w ay w e do things around here”). O ne w ay to accom plish this is by im plem enting
appropriate policies, standards and procedures. The im plem ented changes should be tracked, the effectiveness of the
change response plans should be assessed, and corrective m easures taken as appropriate. This m ight include
enforcing com pliance w here still required.
The com m unication strategy should be m aintained to sustain ongoing aw areness.
5.2.7  P hase 7— Sustain
C hanges are sustained through conscious reinforcem ent, an ongoing com m unication cam paign and continued top
m anagem ent com m itm ent.
In this phase, corrective action plans are im plem ented, lessons learned are captured and know ledge is shared w ith the
broader enterprise.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

P age intentionally left blank
48

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

49

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

C hapter 6
Im plem entation Life C ycle
6.1  Introduction
C ontinual im provem ent of EGIT is accom plished using the seven-phase im plem entation life cycle outlined in
C hapter 3. Each phase is supported by:
A  chart sum m arizing the responsibilities of each group of role players in the phase. The roles defined are generic. 
Not every role necessarily m ust exist as a specific function.
A  table containing: 
Phase objective 
Phase description 
C ontinual im provem ent (C I) tasks 
C hange enablem ent (C E) tasks 
Program  m anagem ent (PM ) tasks 
Exam ples of the inputs likely to be required 
Suggested ISA C A  and other fram ew ork item s to be utilized 
The outputs that need to be produced 
A  chart describing w ho is responsible, accountable, consulted and inform ed (R A C I) for key activities selected 
from  the continual im provem ent (C I), change enablem ent (C E) and program  m anagem ent (PM ) tasks, w ith
corresponding cross references. A ctivities covered in the R A C I chart are the m ost im portant ones: those that
produce deliverables or outputs to the next phase, have a m ilestone attached to them , or are critical to the success
of the overall initiative. Not all activities are included, in the interest of keeping this guidance concise.
This guidance is not intended to be prescriptive. R ather, it constitutes a generic phase and task plan that should be
adapted to suit a specific im plem entation.
This chapter refers to a num ber of steps in the C O BIT ® 201 9 D esign G uide for C I tasks in phases 1 through 3. The
C O BIT ® 201 9 D esign G uide includes m ore detailed guidance on the C I tasks described in this chapter. B oth guides
should be used in conjunction during the initial phases of a governance im provem ent program .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

50
6.2  P hase 1— W hat A re the Drivers?

Figure 6.1 — P hase 1  W hat A re the Drivers?
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
• Change enablement
(middle ring)
• Continual improvement life cycle
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
Defineproblemsand
opportunities
Defineroadmap
Plan program
Executeplan
Realizebenefits
Review
effectiveness
Operate
Identify role
Communicate
team
anduse
players
outcome
Form
implementationEmbednew
Sustain
approaches
Implement
improvementss
state
Assess
Monitor
Operate
improvements Build
target
current
and
and
Define
state
evaluate
measure Continual
improvement
Program
management
Change
enablement
Figure 6.2— P hase 1  R oles
W hen you are... Your role in this phase is to...
Board and executive Provide guidance regarding stakeholder needs (including customer needs), business strategy,
priorities, objectives and guiding principles with respect to EGIT. Approve the high-level approach.
Business management Together with IT, ensure that stakeholder needs and business objectives are stated with suﬃcient
clarity to enable translation into business goals for I&T. Provide input to understanding of risk and
priorities.
IT management Gather requirements and objectives from all stakeholders, gaining consensus on approach and
scope. Provide expert advice and guidance regarding IT matters.
Internal audit Provide advice and challenge proposed activities and actions, ensuring that objective and
balanced decisions are made. Provide input on current issues. Provide advice regarding controls
and risk management practices and approaches.
Risk, compliance and
legal
Provide advice and guidance regarding risk, compliance and legal matters. Ensure that the
management-proposed approach is likely to meet risk, compliance and legal requirements.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

51

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

Figure 6.3 — P hase 1  O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs
Description of Phase 1 — W hat Are the Drivers?
Phase objective Obtain an understanding of the program background and objectives and current governance
approach. Deﬁne the initial program concept business case. Obtain the buy-in and commitment of
all key stakeholders.
Phase description This phase articulates the compelling reasons to act within the organizational context. In this
context, the program background, objectives and current governance culture are deﬁned. The
initial program concept business case is deﬁned. The buy-in and commitment of all key
stakeholders is obtained.
Continual improvement
(CI) tasks
A number of the CI tasks are equivalent to the activities deﬁned in the C O BIT ® 201 9 D esign G uide .
This guide should be consulted for more detailed guidance on the ﬁrst three tasks, and in
particular, the design guide’s Steps 1.1 Understand enterprise strategy , 1.2 Understand enterprise
goals , 1.3 Understand the risk proﬁle and 1.4 Understand current I&T-related issues .
Recognize the need to act:
Identify current governance context, business and IT pain points, events, and symptoms 1 .
triggering the need to act.
Identify the business and governance drivers and compliance requirements for improving 2.
EGIT and assess current stakeholder needs.
Identify business priorities and business strategy dependent on IT, including any current 3 .
signiﬁcant projects.
Align with enterprise policies, strategies, guiding principles and any ongoing governance 4.
initiatives.
Raise executive awareness of IT’s importance to the enterprise and the value of EGIT. 5.
Deﬁne EGIT policy, objectives, guiding principles and high-level improvement targets. 6.
Ensure that the executives and board understand and approve the high-level approach and 7.
accept the risk of not taking any action on signiﬁcant issues.
Change enablement
(CE) tasks
Establish the desire to change:
Ensure integration with enterprise-level change enablement approaches or programs, if any 1 .
exist.
Analyze the general organizational environment in which the change needs to be enabled. 2.
This includes organization structure, management style(s), culture, ways of working, formal
and informal relationships, and attitudes.
Determine other ongoing or planned enterprise initiatives to determine change dependencies 3 .
or impacts.
Understand the breadth and depth of the change. 4.
Identify stakeholders involved in the initiative from different areas of the enterprise (e.g.,5.
business, IT, audit, risk management) as well as different levels (e.g., executives, middle
management) and consider their needs.
Determine the level of support and involvement required from each stakeholder group or 6.
individual, their inﬂuence, and the impact of the change initiative on them.
Determine the readiness and ability to implement the change for each stakeholder group or 7.
individual.
Establish a wake-up call, using the pain points and trigger events as a starting point. Use the 8.
I&T governance board (or an equivalent governance structure) to communicate the message
to create awareness of the program, its drivers and its objectives among all stakeholders.
Eliminate any false signs of security or complacency by, for example, highlighting compliance 9 .
or exception ﬁgures.
Instill the appropriate level of urgency, depending on the priority and impact of the change. 1 0.
Program management
(PM) tasks
Initiate the program:
Provide high-level strategic direction and set high-level program objectives in agreement with 1 .
the I&T governance board or equivalent (if one exists).
Deﬁne and assign high-level roles and responsibilities within the program, starting with the 2.
executive sponsor and including the program manager and all the important stakeholders.
Develop an outline business case indicating the success factors to be used to enable 3 .
performance monitoring and reporting of the success of the governance improvement.
Obtain executive sponsorship. 4.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

52

Figure 6.3 — P hase 1  O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 1 — W hat Are the Drivers?
Input  Enterprise policies, strategies, governance and business plans, and audit reports 
Other major enterprise initiatives on which there may be dependencies or impacts 
I&T governance board performance reports help desk statistics, IT customer surveys or other 
inputs that indicate current IT pain points
Any useful and relevant industry overviews, case studies and success stories (see 
w w w .isaca.org/cobitcasestudies )
Speciﬁc customer requirements, marketing and servicing strategy, market position, enterprise 
vision and mission statements
ISACA materials and
other frameworks
C O BIT ® 201 9 D esign G uide (design factors) 
C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives (particularly EDM01, APO01,
MEA01) and C O BIT ® 201 9 Fram ew ork: Introduction and M ethodology , Chapter 9, Getting Started
With COBIT: Making the Case, w w w .isaca.org/cobit
The example decision matrix in the appendix of this publication 
ISACA supporting products currently listed at w w w .isaca.org 
Output  Business case outline 
High-level roles and responsibilities 
Identiﬁed stakeholder map, including support and involvement required, inﬂuence and impact,
and agreed understanding of the efforts required to manage human change
Program wake-up call (all stakeholders) 
Program kick-off communication (key stakeholders) 
Figure 6.4— P hase 1  R ACI Chart

## Key Activities

Identify is sues triggering need to act (CI1). C/I A R R C C C C R
Identify  business priorities and strategies affecting IT (CI3). C A R R C C C C R
Gain management agreement to act and obtain executive sponsorship (CI7). C A/R R C I I I I R
Ins till the ap propriate level of urgency to change (CE10). I A R R C C C C R
Produce convincing outline business case (PM3). I A R C C C C C R
A RACI char t identif ies who is Responsible, Accountable, Cons ulted and/or  Informed.

## Responsibilities of Implementation Role Pla yers

Board

## I&T Governance Board

# CIO

## Business Executive

## IT Managers

## IT Process Owners

## IT Audit

## Risk and Compliance

## Program Steering

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

53

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

6.3   P hase 2— W here A re W e N ow ?

Figure 6.5— P hase 2 W here A re W e N ow ?
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
• Change enablement
(middle ring)
• Continual improvement life cycle
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
Initiate program
Defineroadmap
Plan program
Executeplan
Realizebenefits
Review
effectiveness
Operate
Identify role
Communicate
to change
anduse
players
outcome
Establish desire
Embednew
Sustain
approaches
Implement
improvementss
state
RecognizeMonitor
Operate
improvements Build
target
need toand
and
Define
act
evaluate
measure
Continualimprovement
Programmanagement
Change enablement
Figure 6.6— P hase 2 R oles
W hen you are... Your role in this phase is to...
Board and executive Verify and interpret the results/conclusions of assessments.
Business management Assist IT in determining the reasonableness of current assessments by providing the customer view.
IT management Ensure open and fair assessment of IT activities. Guide assessment of current practice. Obtain
consensus.
Internal audit Provide advice, input and assistance to current-state assessments. If required, independently
verify assessment results.
Risk, compliance and
legal
Review assessments to ensure that risk, compliance and legal issues have been considered
adequately.
Figure 6.7— P hase 2 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs
Description of Phase 2— W here Are W e N ow ?
Phase objective Ensure that the program team knows and understands the enterprise goals and how the business
and IT function need to deliver value from I&T in support of the enterprise goals, including any
current signiﬁcant projects. Identify the critical processes or other enablers that will be addressed
in the improvement plan. Identify the appropriate management practices for each selected
process. Obtain an understanding of the enterprise’s present and future attitude toward risk and
the IT-risk position, and determine how it will impact the program. Determine the current capability
of the selected processes. Understand the enterprise’s capacity and capability for change.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

54
Figure 6.7— P hase 2 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 2— W here Are W e N ow ?
Phase description This phase identiﬁes the enterprise and alignment goals and illustrates how I&T contributes to
enterprise goals via solutions and services.
The focus is on identifying and analyzing how I&T creates value for the enterprise by enabling
business transformation in an agile way, making the current business processes more eﬃcient,
making the enterprise more effective, and meeting governance-related requirements such as
managing risk, ensuring security, and complying with legal and regulatory requirements.
Based on the enterprise risk proﬁle, its risk history and appetite, and actual beneﬁt/value
enablement risk, deﬁnitions are created for beneﬁt/value enablement risk, program/project
delivery and service delivery/IT operations risk to the enterprise and alignment goals. The C O BIT ®
201 9 D esign G uide contains a table mapping generic risk scenarios to COBIT governance and
management objectives that can be used to support this analysis.
The understanding of business and governance drivers and a risk assessment are used to focus
on the governance and management objectives critical to ensuring that alignment goals are met.
Then, the performance level of the different governance components that support each
governance and management objective are established, based on process descriptions, policies,
standards, procedures and technical speciﬁcations, to determine whether they are likely to
support the business and I&T requirements.
The presence of speciﬁc IT-related issues in an enterprise could also contribute to the selection of
governance and management objectives on which to focus.
The C O BIT ® 201 9 D esign G uide contains an example mapping of common IT-related issues (as
discussed in Chapter 3) to COBIT governance and management objectives.
Continual improvement
(CI) tasks
Assess current state:
Understand how I&T needs to support the current enterprise goals. (A detailed discussion on
enterprise strategies and the COBIT goals cascade is included in the CO BIT ® 201 9 Design G ui de.)
A number of the CI tasks are equivalent to the activities deﬁned in the CO BIT ® 201 9 Design G uide . This
guide should be consulted for more detailed guidance on most of the CI tasks described below.
Identify key enterprise and supporting alignm ent goals —For more detailed guidance, see the
C O BIT ® 201 9 D esign G uide , Section 4, Steps 2.1 C onsider enterprise strategy and 2.2 C onsider
enterprise goals and apply the C O BIT goals cascade .
E stablish the signiﬁcance and nature of I&T’ s contribution (solutions and services) required to 1 .
support business objectives —For more detailed guidance, see the CO BIT ® 201 9 Design G uide ,

## Section 4, Steps 2.2 Consider enterprise goals and apply the CO BIT goals cascade , Step 3.1

Consider enterprise size , Step 3.4 Consider the role of IT , Step 3.5 Consider the sourcing m odel ,
Step 3.6 Consider IT im plem entation m ethods , and Step 3.7 Consider the IT adoption strategy .
Identify key governance issues and w eaknesses related to the current and required future 2.
solutions and services, the enterprise architecture needed to support the IT -related goals —
For more detailed guidance, see the C O BIT ® 201 9 D esign G uide , Section 4, Step 2.4 C onsider
current I&T-related issues .
Identify and select the governance and m anagem ent objectives critical to support IT -related 3 .
goals and, if appropriate, key m anagem ent practices for each selected process —For more
detailed guidance, see the C O BIT ® 201 9 D esign G uide , Section 4, Steps 2.1 C onsider
enterprise strategy and 2.2 C onsider enterprise goals and apply the C O BIT goals cascade .
Assess beneﬁt/value enablem ent risk, program /project delivery and service delivery/IT 4.
operations risk related to critical governance and m anagem ent objectives —For more
detailed guidance, see the C O BIT ® 201 9 D esign G uide , Section 4, Step 2.3 C onsider the risk
proﬁle of the enterprise .
Identify and select governance and m anagem ent objectives critical to ensure that risk is 5.
avoided —For more detailed guidance, see the C O BIT ® 201 9 D esign G uide , Section 4, Step 2.3
C onsider the risk proﬁle of the enterprise .
Understand the risk acceptance position as deﬁned by m anagem ent —For more detailed 6.
guidance, see the C O BIT ® 201 9 D esign G uide , Section 4, Steps 1.3 Understand the risk proﬁle
and 2.3 C onsider the risk proﬁle of the enterprise .

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

55

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

Figure 6.7— P hase 2 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 2— W here Are W e N ow ?
Assess actual performance (refer to C O BIT ® 201 9 Fram ew ork: Introduction and M ethodology ,

## Chapter 6, Performance Management in COBIT):

Deﬁne the method for executing the assessment. See C O BIT ® 201 9 Fram ew ork: Introduction 1 .
and M ethodology , Chapter 6, Performance Management in COBIT.
Document understanding of how the current governance components actually addresses the 2.
management practices selected earlier. See the C O BIT ® 201 9 D esign G uide , all of Steps 2 and
3.
Analyze the current level of capability. See the C O BIT ® 201 9 D esign , Section 4, Step 4, and 3 .
C O BIT ® 201 9 Fram ew ork: Introduction and M ethodology , Chapter 6, Performance
Management in COBIT.
Deﬁne the current process capability rating and the performance levels of other components. 4.
See the C O BIT ® 201 9 D esign G uide , Section 4, Step 4, and C O BIT ® 201 9 Fram ew ork:
Introduction and M ethodology , Chapter 6, Performance Management in COBIT.
Change enablement
(CE) tasks
Form a powerful implementation team:
Assemble a core team from the business and IT with the appropriate knowledge, expertise,1 .
proﬁle, experience, credibility and authority to drive the initiative. Identify the most desirable
person (effective leader and credible to the stakeholders) to lead this team. Consider the use
of external parties, such as consultants, as part of the team to provide an independent and
objective view or to address any skill gaps that may exist.
Identify and manage any potential vested interests that may exist within the team to create 2.
the required level of trust.
Create the appropriate environment for optimal teamwork. This includes ensuring that the 3 .
necessary time and involvement can be given.
Hold a workshop to create consensus (shared vision) within the team and adopt a mandate 4.
for the change initiative.
Identify change agents with whom the core team can work, using the principle of cascading 5.
sponsorship (having sponsors at various hierarchical levels supporting the vision, spreading
the word on quick wins, cascading changes down, and working with any blockers and cynics
that may exist). This will help to ensure widespread stakeholder buy-in during each phase of
the life cycle.
Document strengths identiﬁed during the current-state assessment that can be used for 6.
positive elements in communications as well as potential quick wins that can be leveraged
from a change enablement perspective.
Program management
(PM) tasks
Deﬁne problems and opportunities:
Review and evaluate the outline business case, program feasibility and potential return on 1 .
investment (ROI).
Assign roles, responsibilities and process ownership. Ensure commitment and support of 2.
affected stakeholders in the deﬁnition and execution of the program.
Identify challenges and success factors. 3 .
Input  Outline business case 
High-level roles and responsibilities 
Identiﬁed stakeholder map, including support and involvement required, inﬂuence and impact,
and readiness and ability to implement or buy into the change
Program wake-up call (all stakeholders) 
Program kick-off communication (key stakeholders) 
Business and IT plans and strategies 
IT process descriptions, policies, standards, procedures, technical speciﬁcations 
Understanding of business and IT contribution 
Audit reports, risk management policy, IT performance reports/dashboards/scorecards 
Business continuity plans (BCPs), impact analyses, regulatory requirements, enterprise 
architectures, service level agreements (SLAs), operational level agreements (OLAs)
Investment program and project portfolios, program and project plans, project management 
methodologies, project reports

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

56

Figure 6.8— P hase 2 R ACI Chart

## Key Activities

Identify  key IT goals supporting business goals (CI1). I C R C R C C C A
Identify  processes critical to support IT and business goals (CI4).  I R C R C C C A
Assess risk related to achievement of goals (CI5).  I R C R R C R A
Identify  processes critical to ensure that key risk is avoided (CI6).  I R R R C C R A
Assess current performance of critical processes (CI1 to CI11).  I R C R R C C A
Assemble a core team from the business and IT (CE1).  I R R C C C C A
Review and evaluate the business case (PM1). I A R R C C C C R
A RACI char t identif ies who is Responsible, Accountable, Cons ulted and/or  Informed.

## Responsibilities of Implementation Role Pla yers

Board

## I&T Governance Board

# CIO

## Business Executive

## IT Managers

## IT Process Owners

## IT Audit

## Risk and Compliance

## Program Steering

Figure 6.7— P hase 2 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 2— W here Are W e N ow ?
Output  Agreed alignment goals and impact on I&T 
Agreed understanding of the risk and impacts resulting from misaligned alignment goals and 
service and project delivery failures
Selected governance and management objectives 
Current performance levels of selected governance and management objectives, including 
process capability levels
Risk acceptance position and risk proﬁle 
Beneﬁt/value enablement risk, program/project delivery and service delivery/IT operations risk 
assessments
Strengths on which to build 
Change agents in different parts and at different levels in the enterprise 
Core team and assigned roles and responsibilities 
Evaluated outline business case 
Agreed understanding of the issues and challenges (including process capability levels) 
ISACA resources  C O BIT ® 201 9 Fram ew ork: Introduction and M ethodology (governance and management 
objectives, goals cascade, enterprise goals-alignment goals cascade), w w w .isaca.org/cobit
C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives (APO01, APO02, APO05,
APO12, BAI01, BAI11, MEA01, MEA02, MEA03, MEA04, used for process selection and process
capability assessment, as well as implementation and program planning)

## Chapter 5, Enabling Change, in this publication 

ISACA supporting products as currently listed at w w w .isaca.org 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

57

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

6.4  P hase 3 — W here Do W e W ant to B e?

Figure 6.9 — P hase 3  W here Do W e W ant to Be?
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
• Change enablement
(middle ring)
• Continual improvement life cycle
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
Initiate program
Defineproblemsand
opportunities
Plan program
Executeplan
Realizebenefits
Review
effectiveness
Operate
Identify role
team
to change
anduse
players
Form
implementation
Establish desire
Embednew
Sustain
approaches
Implement
improvementss
Assess
RecognizeMonitor
Operate
improvements Build
current
need toand
and state
act
evaluate
measure
Continual
improvement
Program
management
Change
enablement
Figure 6.1 0 — P hase 3  R oles
W hen you are... Your role in this phase is to...
Board and executive Set priorities, time scales and expectations regarding the future capability required from I&T.
Business management Assist IT with the setting of capability targets. Ensure that the envisaged solutions are aligned to
enterprise goals.
IT management Apply professional judgment in formulating improvement priority plans and initiatives. Obtain
consensus on a required capability target. Ensure that the envisaged solution is aligned to
alignment goals.
Internal audit Provide advice and assist with target-state positioning and gap priorities. If required,
independently verify assessment results.
Risk, compliance and
legal
Review plans to ensure that risk, compliance and legal issues have been addressed adequately.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

58
Figure 6.1 1 — P hase 3  O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs
Description of Phase 3 — W here Do W e W ant to B e?
Phase objective Determine the targeted capability for the processes within each of the selected governance and
management objectives. Determine gaps between the as-is and the to-be positions of the
selected processes and translate these gaps into improvement opportunities. Use this
information to create a detailed business case and high-level program plan.
Phase description Based on the assessed current-state process capability levels, and using the results of the
enterprise goals-to-alignment goals analysis and identiﬁcation of process importance performed
earlier, an appropriate target capability level should be determined for each process. The chosen
level should consider available external and internal benchmarks. It is important to ensure the
appropriateness to the business of the level chosen.
After the current capability of the process has been determined and the target capability planned,
the gaps between the current state and the desired future state should be evaluated and
opportunities for improvement identiﬁed. After the gaps have been deﬁned, the root causes,
common issues, residual risk, existing strengths and good practices to close those gaps need to
be determined.
This phase may identify some relatively easy-to-achieve improvements such as improved training,
sharing good practices and standardizing procedures. However, the gap analysis is likely to
require considerable experience in business and IT-management techniques to develop practical
solutions. Experience in undertaking behavioral and organizational change will also be needed.
Understanding of process techniques, advanced business and technical expertise, and knowledge
of business and system management software applications and services may be needed. To
ensure that this phase is executed effectively, it is important for the team to work with the
business and IT process owners and other required stakeholders, engaging internal expertise. If
necessary, external advice should also be obtained. Risk that will not be mitigated after closing
the gaps should be identiﬁed and formally accepted by management.
Continual improvement
(CI) tasks
CI tasks 1 and 2, described as follows, can build on the results of the governance system design
approach as described in the C O BIT ® 201 9 D esign G uide . This is especially true of governance
system design workﬂow Step 4 (which consists of Steps 4.1 Resolve Inherent priority conﬂicts and
4.2 C onclude the governance system  design ). This step outlines taking an informed and
substantiated decision on target capability and performance levels for the components of the
governance system, which is equivalent to the following CI tasks.

## 1. Deﬁne target for improvement:

Based on enterprise requirements for performance and conformance, decide initial, ideal
short- and long-term target capability levels for each process.
Benchmark internally (to the extent possible) to identify better practices that can be adopted. 
Benchmark externally (to the extent possible) with competitors and peers, to help decide 
appropriateness of the chosen target level.
Do a sanity check on the reasonableness of the targeted levels (individually and as a whole),
looking at what is achievable and desirable, and what can have the greatest positive impact
within the chosen time frame.

## 2. Analyze gaps:

Use understanding of current capability (by attribute) and compare it to the target capability 
level.
Leverage existing strengths wherever possible to deal with gaps. Seek guidance from COBIT 
management practices and activities and other speciﬁc good practices and standards, such
as ITIL ®, ISO/IEC 27000, The Open Group Architectural Framework (TOGAF ®) and Project
Management Body of Knowledge (PMBOK ®) to close other gaps.
Look for patterns that indicate root causes to be addressed. 

## 3. Identify potential improvements:

Collate gaps into potential improvements. 
Identify unmitigated residual risk and ensure its formal acceptance. 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

59

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

Figure 6.1 1 — P hase 3  O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 3 — W here Do W e W ant to B e?
Change enablement
(CE) tasks
Describe and communicate desired outcomes:
Describe the high-level change enablement plan and objectives, which will include the 1 .
following tasks and components.
Develop a communication strategy to optimize awareness and buy-in. The strategy should 2.
include core audience groups, a behavioral proﬁle and information requirements for each
group, core messages, optimal communication channels, and communication principles.
Secure willingness to participate (picture of the change). 3 .
Articulate the rationale for, and beneﬁts of, the change to support the vision. Describe the 4.
impact(s) of not making the change (purpose of the change).
Link back to objectives for the initiative in the communications and demonstrate how the 5.
change will realize the beneﬁt.
Describe the high-level road map to achieve the vision (plan for the change) as well as the 6.
involvement required of various stakeholders (role within the change).
Set the tone at the top by using senior management to deliver key messages. 7.
Use change agents to communicate informally, in addition to formal communications. 8.
Communicate through action. The guiding team should set an example. 9 .
Appeal to people’s emotions to encourage them to change behaviors, when required. 1 0.
Capture initial communication feedback (reactions and suggestions) and adapt the 1 1.
communication strategy accordingly.
Program management
(PM) tasks
Deﬁne the road map:
Set program direction, scope, beneﬁts and objectives at a high level. 1 .
Ensure alignment of the objectives with business and IT strategies. 2.
Consider risk and adjust the scope accordingly. 3 .
Consider change enablement implications. 4.
Obtain necessary budgets and deﬁne program accountabilities and responsibilities. 5.
Create and evaluate a detailed business case, budget, time lines and high-level program plan. 6.
Input  Agreed enterprise goals and impact on alignment goals 
Current capability rating for selected processes 
Deﬁnition of alignment goals 
Selected processes and goals 
Risk acceptance position and risk proﬁle 
Assessed beneﬁt/value enablement risk, program/project delivery and service delivery/IT 
operations risk assessment
Strengths on which to build 
Change agents in different parts and at different levels in the enterprise 
Core team and assigned roles and responsibilities 
Evaluated outline business case 
Challenges and success factors 
Internal and external capability benchmarks 
Good practices from COBIT and other references 
Stakeholder analysis 
Output  Target capability rating for selected processes 
Description of improvement opportunities 
Risk response document, including risk not mitigated 
Change enablement plan and objectives 
Communication strategy and communication of the change vision covering the four Ps (picture,
purpose, plan, part)
Detailed business case 
High-level program plan 
Key metrics that will be used to track program and operational performance 
ISACA resources  C O BIT ® 201 9 Fram ew ork: Introduction and M ethodology (enterprise goals), w w w .isaca.org/cobit 
C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives (management practices and 
activities for the target-state deﬁnition and gap analysis, APO01, APO02)
ISACA supporting products, as currently listed at w w w .isaca.org 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

60

6.5   P hase 4— W hat N eeds to B e Done?

Figure 6.1 2— P hase 3  R ACI Chart

## Key Activities

Agr ee on tar get for imp r o v e m e n t  ( C I 1 ) .  I  A  R  C  R  R  C  C  R

## Analy ze gaps (CI2).  I R C R R C C A

## Identify  potential improvements (CI3).  I R C R R C C A

Commu nicate change vision (CE3).  A  R  R  C  I  I  I  R
Set p rogram direction and prepare detailed business case (PM1, PM6). I A R C C C I I R
A RACI char t identif ies who is Responsible, Accountable, Cons ulted and/or  Informed.

## Responsibilities of Implementation Role Pla yers

Board

## I&T Governance Board

# CIO

## Business Executive

## IT Managers

## IT Process Owners

## IT Audit

## Risk and Compliance

## Program Steering

Figure 6.1 3 — P hase 4 W hat N eeds to Be Done?
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
• Change enablement
(middle ring)
• Continual improvement life cycle
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
Initiate program
Defineproblemsand
opportunities
DefineroadmapExecuteplan
Realizebenefits
Review
effectiveness
Operate
Communicate
team
to change
anduse outcome
Form
implementation
Establish desire
Embednew
Sustain
approaches
Implement state
Assess
RecognizeMonitor
Operate
improvements
target
current
need toand
and
Define
state
act
evaluate
measure
Continual
improvement
Program
management
Change
enablement

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

61

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

Figure 6.1 4— P hase 4 R oles
W hen you are... Your role in this phase is to...
Board and executive Consider and challenge proposals, support justiﬁed actions, provide budgets, and set priorities as
appropriate.
Business management Together with IT, ensure that the proposed improvement actions are aligned with agreed
enterprise and IT-related goals and that any activities requiring business input or action are
supported. Ensure that required business resources are allocated and available. Agree with IT on
the metrics for measuring the outcomes of the improvement program.
IT management Ensure viability and reasonableness of the program plan. Ensure that the plan is achievable, and
resources are available to execute the plan. Consider the plan together with priorities of the
enterprise’s portfolio of I&T-enabled investments to decide a basis for investment funding.
Internal audit Provide independent assurance that issues identiﬁed are valid, business cases are objectively and
accurately presented, and plans appear achievable. Provide expert advice and guidance where
appropriate.
Risk, compliance and
legal
Ensure that any identiﬁed risk, compliance and legal issues are being addressed, and that
proposals conform with any relevant policies or regulations.
Figure 6.1 5— P hase 4 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs
Description of Phase 4— W hat N eeds to B e Done?
Phase objective Translate improvement opportunities into justiﬁable contributing projects. Prioritize and focus on
high-impact projects. Integrate the improvement projects into the overall program plan. Execute
quick wins.
Phase description When all the potential initiatives for improvement have been identiﬁed, they should be prioritized
into formal and justiﬁable projects. The projects that are of high beneﬁt and relatively easy to
implement should be selected ﬁrst, and translated into formal and justiﬁable projects. Each
should have a project plan that includes the project’s contribution to program objectives. It is
important to check whether the objectives still conform to the original value and risk drivers. The
projects will be included in an updated business case for the program. Details of any unapproved
project proposals should be recorded in a register for potential future consideration.  Sponsors
may reappraise, and, when appropriate, resubmit new recommendations at a later date.
Based on an opportunity grid, the project deﬁnitions, the resource plan and the I&T budget, the
identiﬁed and prioritized improvements are now turned into a set of documented projects that
support the overall improvement program. The impact on the enterprise of executing the program
is determined and a change plan is prepared that describes the program activities that will ensure,
in practical terms, that the improvements delivered by the projects will be rolled into the enterprise
in a sustainable manner. An important element in this phase is the deﬁnition of metrics—that is,
the program’s success metrics—that will measure whether the process improvements are likely to
deliver the original business beneﬁts. The complete improvement program schedule should be
documented on a Gantt chart.
New projects may identify a need to change or improve the organizational structures or other
enablers required to sustain effective governance. If required, it may be necessary to include
actions to improve the environment (as described in Chapter 5).

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

62
Figure 6.1 5— P hase 4 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 4— W hat N eeds to B e Done?
Continual improvement
(CI) tasks
Design and build improvements:
Consider potential beneﬁt and ease of implementation (cost, effort and sustainability) for 1 .
each improvement.
Plot improvements onto an opportunity grid to identify priority actions (based on beneﬁt and 2.
ease of implementation).
Focus on alternatives showing high beneﬁt/high ease of implementation. 3 .
Consider alternatives showing high beneﬁt/low ease of implementation for possible scaled- 4.
down improvements. Decompose them into smaller improvements and look again at beneﬁts
and ease of implementation.
Prioritize and select improvements. 5.
Analyze selected improvements to the detail required for high-level project deﬁnition. 6.
Consider approach, deliverables, resources required, estimated costs, estimated time scales,
dependencies and project risk. Use available good practices and standards to further reﬁne
detailed improvement requirements. Discuss with managers and teams responsible for the
process area.
Consider feasibility, link back to the original value and risk drivers, and agree on projects to be 7.
included in the business case for approval.
Record unapproved projects and initiatives in a register for potential future consideration. 8.
Change enablement
(CE) tasks
Empower role players and identify quick wins:
Obtain buy-in by engaging affected users through mechanisms such as workshops or review 1 .
processes. Give them responsibility to accept the quality of results.
Design change response plans to proactively manage change impacts and maximize 2.
engagement throughout the implementation process. This could include organizational
changes, such as job content or organizational structure; people management changes, such
as training; performance management systems; or incentives/remuneration and reward
systems.
Identify quick wins that prove the concept of the improvement program. These should be 3 .
visible and unambiguous, build momentum, and provide positive reinforcement of the
process.
Build on any existing strengths identiﬁed in phase 2 to realize quick wins, where possible. 4.
Identify strengths in existing enterprise processes that could be leveraged. For example,5.
strengths in project management may exist in other areas of the business, such as product
development. Avoid reinventing the wheel and align wherever possible to current
enterprisewide approaches.
Program management
(PM) tasks
Develop the program plan:
Organize potential projects into the overall program, in preferred sequence, considering 1 .
contribution to desired outcomes, resource requirements and dependencies.
Use portfolio management techniques to ensure that the program conforms to strategic 2.
goals and that I&T has a balanced set of initiatives.
Identify the impact of the improvement program on the IT and business organizations and 3 .
indicate how the improvement momentum is to be maintained.
Develop a change plan documenting any migration, conversion, testing, training, process or 4.
other activities that must be included within the program as part of implementation.
Identify and agree on metrics for measuring the outcomes of the improvement program in 5.
terms of the original program success factors.
Guide the allocation and prioritization of business, IT and audit resources necessary to 6.
achieve program and project objectives.
Deﬁne a portfolio of projects that will deliver required outcomes for the program. 7.
Deﬁne required deliverables, considering the full scope of activities needed to meet 8.
objectives.
Nominate project steering committees for speciﬁc projects within the program, if required. 9 .
Establish project plans and reporting procedures to enable progress to be monitored. 1 0.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

63

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

Figure 6.1 6— P hase 4 R ACI Chart

## Key Activities

Prioritiz e and select imp r o v e m e n t s  ( C I 5 ) .   A  R  C  C  R  C  C  R
Define and ju stify projects (CI6 and CI7).  I R C R R C C A
Design change r esponse plans (CE2).  I R R C C C C A
Identify qu ick wins  and b uild on existing strengths (CE3).  I C C/I R R C/I C/I A
Develop program plan with allocated resources and project plans (PM1 to PM10).  A  C  C  R  C  I  I  R
A RACI char t identifies who is Responsible, Accountable, Consulted and/or Informed.

## Responsibilities of Implementation Role Pla yers

Board

## I&T Governance Board

# CIO

## Business Executive

## IT Managers

## IT Process Owners

## IT Audit

## Risk and Compliance

## Program Steering

Figure 6.1 5— P hase 4 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 4— W hat N eeds to B e Done?
Input  Target maturity rating for selected processes 
Description of improvement opportunities 
Risk response document 
Change enablement plan and objectives 
Communication strategy and communication of the change vision covering four Ps (picture,
purpose, plan, part)
Detailed business case 
Opportunity worksheet, good practices and standards, external assessments, technical
evaluations
Opportunity grid, project deﬁnitions, project portfolio management plan, resource plan, I&T 
budget
Strengths identiﬁed in earlier phases 
Output  Improvement project deﬁnitions 
Deﬁned change response plans 
Identiﬁed quick wins 
Record of unapproved projects 
Program plan that sequences individual plans with allocated resources, priorities and 
deliverables
Project plans and reporting procedures enabled through committed resources such as skills 
and investment
Success metrics 
ISACA resources  C O BIT ® 201 9 Fram ew ork: Introduction and M ethodology (governance and management 
objectives, components of the governance system), w w w .isaca.org/cobit
C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives (APO5, APO12, BAI01, BAI11,
goals and metrics)
ISACA supporting products as currently listed at w w w .isaca.org 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

64
6.6  P hase 5 — H ow  Do W e Get There?

Figure 6.1 7— P hase 5 H ow  Do W e G et There?
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
• Change enablement
(middle ring)
• Continual improvement life cycle
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
Initiate program
Defineproblemsand
opportunities
Defineroadmap
Plan program
Realizebenefits
Review
effectiveness
Identify role
Communicate
team
to change
players
outcome
Form
implementation
Establish desire
Embednew
Sustain
approaches
improvementss
state
Assess
RecognizeMonitor
Operate
Build
target
current
need toand
and
Define
state
act
evaluate
measure
g
Continual
improvement
Program
management
Change
enablement
Figure 6.1 8— P hase 5 R oles
W hen you are... Your role in this phase is to...
Board and executive Monitor implementation and provide support and direction as required.
Business management Take ownership for business participation in the implementation, especially where business
processes are affected, and IT processes require user/customer involvement.
IT management Make sure that the implementation includes the full scope of activities required (e.g., policy and
process changes, technology solutions, organizational changes, new roles and responsibilities,
other enablers); ensure that implementations are practical, achievable, and likely to be adopted
and used. Make sure that process owners are involved, buy into the new approach and own the
resulting processes. Resolve issues and manage risk as encountered during the implementation.
Internal audit Review and provide input during implementation to avoid after-the-fact identiﬁcation of missing
enablers and especially key controls. Provide guidance on implementation of control aspects. If
required, provide a project/implementation risk review service, monitoring risk that could
jeopardize implementation and providing independent feedback to the program and project
teams.
Risk, compliance and
legal
Provide guidance as required on risk, compliance and legal aspects during implementation.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

65

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

Figure 6.1 9 — P hase 5 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs
Description of Phase 5— H ow  Do W e G et There?
Phase objective Implement the detailed improvement projects, leveraging enterprise program and project
management capabilities, standards and practices. Monitor, measure and report on project
progress.
Phase description The approved improvement projects, including required change activities, are now ready for
implementation, so the solutions deﬁned by the program can now be acquired or developed and
implemented into the enterprise. In this way, projects become part of the normal development life
cycle and should be governed by established program and project management methods. The
rollout of the solution should align with the established project deﬁnitions and change plan to
support the improvements’ sustainability.
This phase typically involves the most effort and longest elapsed time of all the life cycle phases.
However, it is important to ensure that the phase is manageable and beneﬁts are delivered in a
reasonable time frame, so excessive size and overall time taken should be avoided. This is
especially true for the ﬁrst few iterations, which will also be a learning experience for all involved.
Performance of each project must be monitored to ensure that goals are being achieved.
Reporting back to stakeholders at regular intervals ensures that progress is understood and on
track.
Continual improvement
(CI) tasks
Implement improvements:
Develop and, where necessary, acquire solutions that include the full scope of activities 1 .
required. These may include culture, ethics and behavior; organizational structures; principles
and policies; processes; service capabilities; skills and competencies; and information.
When using good practices, adopt and adapt available guidance to suit the enterprise’s 2.
approach to policies and procedures.
Test the practicality and suitability of the solutions in the real working environment. 3 .
Roll out the solutions, considering any existing processes and migration requirements. 4.
Change enablement
(CE) tasks
Enable operation and use:
Build on the momentum and credibility that can be created by quick wins, then introduce 1 .
more widespread and challenging change aspects.
Communicate quick-win successes and recognize and reward those involved in them. 2.
Implement the change response plans. 3 .
Ensure that the broader base of role players has the skills, resources and knowledge, as well4.
as buy-in and commitment to the change.
Balance group and individual interventions to ensure that key stakeholders obtain a holistic 5.
view of the change.
Plan cultural and behavioral aspects of the broader transition (dealing with fears of loss of 6.
responsibility/independence/decision authority, new expectations and unknown tasks).
Communicate roles and responsibilities for use. 7.
Deﬁne measures of success, including those from a business viewpoint and perception 8.
measures.
Set in place mentoring and coaching to ensure uptake and buy-in. 9 .
Close the loop and ensure that all change requirements have been addressed. 1 0.
Monitor the change enablement effectiveness and take corrective action where necessary. 1 1.
Program management
(PM) tasks
Execute the plan:
Ensure that the execution of the program is based on an up-to-date and integrated (business 1 .
and IT) plan of the projects within the program.
Direct and monitor the contribution of all the projects in the program to ensure delivery of the 2.
expected outcomes.
Provide regular update reports to stakeholders to ensure that progress is understood and on 3 .
track.
Document and monitor signiﬁcant program risk and issues and agree on remediation actions. 4.
Approve the initiation of each major program phase and communicate it to all stakeholders. 5.
Approve any major changes to the program and project plans. 6.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

66

Figure 6.20 — P hase 5 R ACI Chart

## Key Activities

Develop and, if required, acquire solutions (CI1).  A C C R R C C R
Adopt and adap t good p ractices (CI2).  I R C R R C C A
Test and roll out solutions (CI3 and CI4).  I R C R R C C A
Capitaliz e on qu ick wins  (CE1 and CE2).  I  C  C / I  R  R  C / I  C / I  A
Imp lement change r esponse plans (CE3). I I R C R R I I A
Dir ect and monit or p rojects within the program (PM2). I A C C R C I I R
A RACI char t identif ies who is Responsible, Accountable, Cons ulted and/or  Informed.

## Responsibilities of Implementation Role Pla yers

Board

## I&T Governance Board

# CIO

## Business Executive

## IT Managers

## IT Process Owners

## IT Audit

## Risk and Compliance

## Program Steering

Figure 6.1 9 — P hase 5 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 5— H ow  Do W e G et There?
Input  Improvement project deﬁnitions 
Deﬁned change response plans 
Identiﬁed quick wins 
Record of unapproved projects 
Program plan with allocated resources, priorities and deliverables 
Project plans and reporting procedures 
Success metrics 
Project deﬁnitions, project Gantt chart, change response plans, change strategy 
Integrated program and project plans 
Output  Implemented improvements 
Implemented change response plans 
Realized quick wins and visibility of change success 
Success communications 
Deﬁned and communicated roles and responsibilities in the business-as-usual environment 
Project change logs and issue/risk logs 
Deﬁned business and perception success measures 
Beneﬁts tracked to monitor realization 
ISACA resources  C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives (all objectives as good 
practice input, BAI01, BAI11), w w w .isaca.org/cobit
ISACA supporting products as currently listed at w w w .isaca.org 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

67

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

6.7  P hase 6— Did W e Get There?

Figure 6.21 — P hase 6 Did W e G et There?
the momentum going?
7 How do we keep
6 Did we get there?
5 How do we get there?
4 What needs to be done?
3 Where do we want to be?
2 Where are we now?
1 What are the drivers?
• Program management
(ou ter ring)
• Change enablement
(mi ddle ring)
• Continual improvement life cycle
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
Initiate program
Defineproblemsand
opportunities
Defineroadmap
Plan program
Executeplan
Review
effectiveness
Operate
Identify role
Communicate
team
to change
anduse
players
outcome
Form
implementation
Establish desireSustain
Implement
improvementss
state
Assess
RecognizeMonitor
improvements Build
target
current
need toand
Define
state
act
evaluateContinual
improvement
Program
management
Change
enablement
Figure 6.22— P hase 6 R oles
W hen you are... Your role in this phase is to...
Board and executive Assess performance in meeting the original objectives and conﬁrm realization of desired
outcomes. Consider the need to redirect future activities and take corrective action. Assist in the
resolution of signiﬁcant issues, if required.
Business management Provide feedback and consider the effectiveness of the business’s contribution to the initiative.
Use positive results to improve current business-related activities. Use lessons learned to adapt
and improve the business’s approach to future initiatives.
IT management Provide feedback and consider the effectiveness of IT’s contribution to the initiative. Use positive
results to improve current IT-related activities. Monitor projects based on project criticality as they
are developing, using both program management and project management techniques. Be
prepared to change the plan and/or cancel one or more projects or take other corrective action, if
early indications show that a project is off track and may not meet critical milestones. Use
lessons learned to adapt and improve IT’s approach to future initiatives.
Internal audit Provide independent assessment of the overall eﬃciency and effectiveness of the initiative.
Provide feedback and consider the effectiveness of audit’s contribution to the initiative. Use
positive results to improve current audit-related activities. Use lessons learned to adapt and
improve audit’s approach to future initiatives.
Risk, compliance and
legal
Assess whether the initiative has improved the ability of the enterprise to identify and manage risk
and legal, regulatory and contractual requirements. Provide feedback and make any necessary
recommendations for improvements.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

68
Figure 6.23 — P hase 6 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs
Description of Phase 6— Did W e G et There?
Phase objective Integrate the metrics for project performance and beneﬁts realization of the overall governance
improvement program into the performance measurement system for regular and ongoing
monitoring.
Phase description It is essential that the improvements described in the program be monitored via alignment goals
and process goals using suitable techniques such as an IT balanced scorecard (BSC) and
beneﬁts register to verify that the change outcomes have been achieved. This ensures that the
initiatives remain on track according to original enterprise and alignment goals and continue to
deliver the desired business beneﬁts. For each metric, targets need to be set, compared regularly
against reality and communicated using a performance report.
To ensure success, it is crucial that positive and negative results from performance
measurements be reported to all stakeholders, to build conﬁdence and enable any corrective
actions to be taken on time. Projects should be monitored as they are developing, using both
program management and project management techniques. Preparation should be made to
change the plan and/or cancel the project, if early indications show that a project is off track and
may not meet critical milestones.
Continual improvement
(CI) tasks
Operate and measure:
Set targets for each metric for an agreed time period. Targets should enable monitoring of 1 .
I&T performance and improvement actions and determine success or failure.
Obtain current, actual measures for these metrics, where possible. 2.
Gather actual measures and compare them to targets on a regular basis (e.g., monthly). 3 .
Investigate any signiﬁcant variances.
Develop and agree on proposed corrective measures, wherever variances indicate that 4.
corrective actions are required.
Adjust long-term targets based on experience, if required. 5.
Communicate both positive and negative results from performance monitoring to all6.
interested stakeholders. Include recommendations for any corrective measures.
Change enablement
(CE) tasks
Embed new approaches:
Ensure that new ways of working become part of the enterprise’s culture. They should be 1 .
rooted in the enterprise’s norms and values. This is important for concrete results to be
achieved.
In transitioning from project mode to business as usual, shape behaviors through revised job 2.
descriptions, job performance criteria and associated incentive and reward systems, KPIs,
and operating procedures as implemented through the change-response plans.
Monitor whether assigned roles and responsibilities have been assumed. 3 .
Track the change and assess the effectiveness of the change-response plans, linking the 4.
results back to the original change objectives and goals. This should include both hard
business measures and perception measures, such as perception surveys, feedback
sessions and training evaluation forms.
Leverage pockets of excellence to provide a source of inspiration. 5.
Maintain the communication strategy to achieve ongoing awareness and highlight 6.
successes.
Ensure that there is open communication among all role players to resolve issues. 7.
Escalate to sponsors, if issues cannot be resolved. 8.
Enforce change through management authority, where still required. 9 .
Document change enablement lessons learned for future implementation initiatives. 1 0.
Program management
(PM) tasks
Realize beneﬁts:
Monitor overall performance of the program against business case objectives. 1 .
Monitor investment performance (cost against budget, realization of beneﬁts). 2.
Document lessons learned (both positive and negative) for subsequent improvement 3 .
initiatives.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

69

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

Figure 6.24— P hase 6 R ACI Chart

## Key Activities

Operate the solutions and gain performance feedback (CI1 to CI3).  I A R R R I I I
Monitor performance against success metrics (CI4 to CI5).  I A C R R C C I
Commu nicate p ositive and negative results (CI6). I I A C R C I I I

## Monitor ownership of roles and responsibilities (CE3).  A R C C C C C I

Monitor program results (achievement of goals and realization of benefits)  I A C C C C C C R
(PM 1 and PM 2).
A RACI char t identif ies who is Responsible, Accountable, Cons ulted and/or  Informed.

## Responsibilities of Implementation Role Pla yers

Board

## I&T Governance Board

# CIO

## Business Executive

## IT Managers

## IT Process Owners

## IT Audit

## Risk and Compliance

## Program Steering

Figure 6.23 — P hase 6 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 6— Did W e G et There?
Input  Implemented improvements 
Implemented change response plans 
Realized quick wins and success communications 
Deﬁned and communicated roles and responsibilities in the business-as-usual environment 
Project change logs and issue/risk logs 
Deﬁned business and perception success measures 
Alignment goals and IT process goals identiﬁed as a result of requirements analysis 
Existing measures and/or scorecards 
Business case beneﬁts 
Change response plans and communication strategy 
Output  Updated project and program scorecards 
Change effectiveness measures (both business and perception measures) 
Report explaining scorecard results 
Improvements entrenched in operations 
Key metrics added into ongoing IT performance measurement approach 
ISACA resources  C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives (as good practice input and 
EDM05, APO05, BAI01, BAI11, MEA01), w w w .isaca.org/cobit
ISACA supporting products as currently listed at w w w .isaca.org 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

70
6.8  P hase 7— H ow  Do W e Keep the M om entum  Going?

Figure 6.25— P hase 7 H ow  Do W e Keep the M om entum  G oing?
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
• Change enablement
(middle ring)
• Con tinual improvement life cycle
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
Initiate program
Defineproblemsand
opportunities
Defineroadmap
Plan program
Executeplan
Realizebenefits
Operate
Identify role
Communicate
team
to change
anduse
players
outcome
Form
implementation
Establish desire
Embednew
approaches
Implement
improvementss
state
Assess
Recognize
Operate
improvements Build
target
current
need to
and
Define
state
act
measure
Continual
improvement
Program
management
Change
enablement
Figure 6.26— P hase 7 R oles
W hen you are... Your role in this phase is to...
Board and executive Provide direction, set objectives, and allocate roles and responsibilities for the enterprise’s
ongoing approach to, and improvement of, EGIT. Continue to set the tone at the top, develop
organizational structures, and encourage a culture of good governance and accountability for I&T
among business and IT executives. Ensure that IT is aware of and, as appropriate, involved in, new
business objectives and requirements in as timely a manner as possible.
Business management Provide support and commitment by continuing to work positively with IT to improve EGIT and
make it business as usual. Verify that new EGIT objectives are aligned with current enterprise
objectives.
IT management Drive and provide strong leadership to sustain the momentum of the improvement program.
Engage in governance activities as part of normal business practice. Create policies, standards
and processes to ensure that governance becomes business as usual.
Internal audit Provide objective and constructive input, encourage self-assessment, and provide assurance to
management that governance is working effectively, thus building conﬁdence in I&T. Provide
ongoing audits based on an integrated governance approach, using criteria shared with IT and the
business based on the COBIT ® 2019 framework.
Risk, compliance and
legal
Work with IT and the business to anticipate legal and regulatory requirements. Identify and
respond to I&T-related risk as a normal activity in EGIT.

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

71

# C H A P TE R  6

# IM P LE M E N T A TIO N  LIF E  C YC LE

Figure 6.27— P hase 7 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs
Description of Phase 7— H ow  Do W e Keep the M om entum  G oing?
Phase objective Assess the results and experience gained from the program. Record and share any lessons
learned. Improve organizational structures, processes, roles and responsibilities to change the
enterprise’s behavior so that EGIT becomes business as usual and is continually optimized.
Ensure that new, required actions drive further iterations of the life cycle.
Continually monitor performance and ensure that results are regularly reported. Drive
commitment and ownership of all accountabilities and responsibilities.
Phase description This phase enables the team to determine whether the program delivered against expectations.
This can be done by comparing the results to the original success criteria and gathering feedback
from the implementation team and stakeholders via interviews, workshops and satisfaction
surveys. The lessons learned can contain valuable information for team members and project
stakeholders for use in ongoing initiatives and improvement projects. It involves continual
monitoring, regular and transparent reporting, and conﬁrmation of accountabilities.
Further improvements are identiﬁed and used as input to the next iteration of the life cycle.
In this phase, the enterprise should build on the successes and lessons learned from the
governance implementation project(s) to build and reinforce commitment among all IT and
business stakeholders for continually improved governance of I&T.
Policies, organizational structures, roles and responsibilities, and governance processes should
be developed and optimized so that EGIT operates effectively as part of normal business practice
and the culture, demonstrated by top management, supports this.
Continual improvement
(CI) tasks
Monitor and evaluate:
Identify new governance objectives and requirements based on experiences gained, current 1 .
business objectives for I&T or other trigger events.
Gather feedback and perform a stakeholder satisfaction survey. 2.
Measure and report actual results against originally established project measures of 3 .
success. Embed continual monitoring and reporting.
Perform a facilitated project review process with project team members and project 4.
stakeholders to record and pass on lessons learned.
Look for additional high-impact, low-cost opportunities to further improve EGIT. 5.
Identify lessons learned. 6.
Communicate requirements for further improvements to the stakeholders and document 7.
them for use as input to the next iteration of the life cycle.
Change enablement
(CE) tasks
Sustain:
Provide conscious reinforcement and an ongoing communication campaign, as well as 1 .
demonstrated continual top management commitment.
Conﬁrm conformance to objectives and requirements. 2.
Continually monitor the effectiveness of the change itself, change enablement activities and 3 .
buy-in of stakeholders.
Implement corrective action plans where required. 4.
Provide feedback on performance, reward achievers and publicize successes. 5.
Build on lessons learned. 6.
Share knowledge from the initiative to the broader enterprise. 7.
Program management
(PM) tasks
Review program effectiveness:
At program closure, ensure that a program review takes place and approve conclusions. 1 .
Review program effectiveness. 2.
Input  Updated project and program scorecards 
Change effectiveness measures (both business and perception measures) 
Report explaining scorecard results 
Postimplementation review report 
Performance reports 
Business and IT strategy 
New triggers such as new regulatory requirements 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

72

Figure 6.28— P hase 7 R ACI Chart

## Key Activities

Identify new go vernance objectives (CI1). C A R R C C C C I
Identify les sons learned (CI2).  I A C R R C C I

## Sustain and reinforce changes (CE1).  A R R R R C C I

Confirm conformance t o objectiv es and requirements (CE2). I A R C R R R I R
Clos e p rogram with formal review of effectiveness (PM1). I A C C C C C C R
A RACI char t identif ies who is Responsible, Accountable, Cons ulted and/or  Informed.

## Responsibilities of Implementation Role Pla yers

Board

## I&T Governance Board

# CIO

## Business Executive

## IT Managers

## IT Process Owners

## IT Audit

## Risk and Compliance

## Program Steering

Figure 6.27— P hase 7 O bjectives, D escriptions, Tasks, Inputs, R esources and O utputs (cont.)
Description of Phase 7— H ow  Do W e Keep the M om entum  G oing?
Output  Recommendations for further EGIT activities after a period of normalization 
Stakeholder satisfaction survey 
Documented success stories and lessons learned 
Ongoing communication plan 
Performance reward scheme 
ISACA resources  C O BIT ® 201 9 Fram ew ork: G overnance and M anagem ent O bjectives (EDM01, APO01, BAI08,
MEA01), w w w .isaca.org/cobit
ISACA supporting products as currently listed at w w w .isaca.org 

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

73

# A P P E N DIX  A

# E X A M P LE  DE C ISIO N  M A TR IX

# A P P E N DIX  A

Exam ple Decision M atrix
This appendix show s an exam ple of how  to identify key topic areas requiring clear decision-m aking roles and
responsibilities. It is provided as a guide and can be m odified and adapted to suit an enterprise’s specific organization
and requirem ents. 14
1

1
14 This exam ple is based on the EGIT m atrix developed by IT W inners. It is used w ith their perm ission.
2
15 IT m anagem ent includes all roles w ithin the IT function at a m anagem ent level.
Figure A.1 — Exam ple D ecision M atrix

## Decision Topic Scope

Responsible, A ccountable,
C onsulted, Inform ed (RA C I)
Executive C om m ittee

## I& T G overnance Board

Enterprise Risk C om m ittee
Portfolio M anager
Steering (Program s/Projects) C om m ittee
IT M anagem ent 15
2
Business Process O w ners
Em ployees
Governance  Integrating with enterprise governance 
Establishing principles, structures, objectives 

# A/R R C C R I

Enterprise strategy  Deﬁning enterprise goals and objectives 
Deciding where and how I&T can enable and support 
enterprise objectives

# A/R R C C R I

I&T policies  Providing accurate, understandable and approved policies,
procedures, guidelines and other documentation to
stakeholders
Developing and rolling out I&T policies 
Ensuring that policies result in beneﬁcial outcomes in 
accordance with guiding principles
Enforcing I&T policies 

# I A C R C C

I&T strategy  Incorporating IT and business management in the 
translation of business requirements into service offerings
and developing strategies to deliver these services in a
transparent and effective manner
Engaging with business and senior management in 
aligning I&T strategic planning with current and future
business needs
Understanding current I&T capabilities 
Providing a prioritization scheme for business objectives 
that quantiﬁes business requirements

# I A C I R C C

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

74
3
15 IT m anagem ent includes all roles w ithin the IT function at a m anagem ent level.
Figure A.1 — Exam ple D ecision M atrix (cont.)

## Decision Topic Scope

Responsible, A ccountable,
C onsulted, Inform ed (RA C I)
Executive C om m ittee

## I& T G overnance Board

Enterprise Risk C om m ittee
Portfolio M anager
Steering (Program s/Projects) C om m ittee
IT M anagem ent 15
3
Business Process O w ners
Em ployees
I&T direction  Providing appropriate platforms for the business 
applications and services in line with the deﬁned I&T
architecture and information & technology standards
Producing an information and technology provisioning 
plan

# I C C A/R C C

I&T methods and
frameworks
Establishing transparent, ﬂexible and responsive IT 
organizational structures and deﬁning and implementing
I&T processes that integrate owners, roles and
responsibilities into business and decision processes
Deﬁning a practical I&T process framework 
Establishing appropriate organizational bodies and 
structure
Deﬁning roles and responsibilities 

# I C C I I A/R I I

Enterprise
architecture
Deﬁning and implementing architecture and standards 
that recognize and leverage technology opportunities
Establishing a forum to guide architecture and verify 
compliance
Establishing the architecture plan balanced against cost,
risk and requirements
Deﬁning the information architecture, including the 
establishment of an enterprise data model that
incorporates a data classiﬁcation scheme
Ensuring the accuracy of the information architecture and 
data model
Assigning data ownership 
Classifying information using an agreed classiﬁcation 
scheme

# A C C I I R R C

I&T-enabled
investment and
portfolio
prioritization
Making effective and eﬃcient I&T-enabled investment and 
portfolio decisions
Forecasting and allocating budgets 
Deﬁning formal investment criteria 
Measuring and assessing business value against forecast 

# I A C C R

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

75

# A P P E N DIX  A

# E X A M P LE  DE C ISIO N  M A TR IX

3
15 IT m anagem ent includes all roles w ithin the IT function at a m anagem ent level.
Figure A.1 — Exam ple D ecision M atrix (cont.)

## Decision Topic Scope

Responsible, A ccountable,
C onsulted, Inform ed (RA C I)
Executive C om m ittee

## I& T G overnance Board

Enterprise Risk C om m ittee
Portfolio M anager
Steering (Program s/Projects) C om m ittee
IT M anagem ent 15
3
Business Process O w ners
Em ployees
I&T-enabled
investment and
program
prioritization
Setting and tracking I&T budgets in line with I&T strategy 
and investment decisions
Measuring and assessing business value against forecast 
Deﬁning a program and project management approach 
that is applied to I&T-enabled business projects and
enables stakeholder participation in, and monitoring of,
project risk and progress
Deﬁning and enforcing program and project frameworks 
and approach
Issuing project management guidelines 
Performing project planning for each project detailed in 
the project portfolio

# I A R C C/I C/I C/I

Managing,
monitoring and
evaluating SLAs
Identifying service requirements, agreeing on service 
levels and monitoring the achievement of service levels
Formalizing internal and external agreements in line with 
requirements and delivery capabilities
Reporting on service level achievements (reports and 
meetings)
Identifying and communicating new and updated service 
requirements to strategic planning
Meeting operational service levels for scheduled data 
processing, protecting sensitive output, and monitoring
and maintaining infrastructure

# I A R R R I

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

76
3
15 IT m anagem ent includes all roles w ithin the IT function at a m anagem ent level.
Figure A.1 — Exam ple D ecision M atrix (cont.)

## Decision Topic Scope

Responsible, A ccountable,
C onsulted, Inform ed (RA C I)
Executive C om m ittee

## I& T G overnance Board

Enterprise Risk C om m ittee
Portfolio M anager
Steering (Program s/Projects) C om m ittee
IT M anagem ent 15
3
Business Process O w ners
Em ployees
IT application
management
Identifying technically feasible and cost-effective 
solutions
Deﬁning business and technical requirements 
Undertaking feasibility studies as deﬁned in the 
development standards
Approving (or rejecting) requirements and feasibility study 
results
Ensuring that there is a timely and cost-effective 
development or acquisition process
Translating business requirements into design 
speciﬁcations
Selecting appropriate development and maintenance 
standards (waterfall, Agile, DevOps, etc.) and adhering to
the standards for all modiﬁcations
Separating development, testing and operational activities 

# I I C A/R C C

IT infrastructure  Operating the IT environment in line with agreed service 
levels and deﬁned instructions
Maintaining the IT infrastructure 

# I I C A/R C C

I&T security  Deﬁning I&T security policies, plans and procedures and 
monitoring, detecting, reporting and resolving security
vulnerabilities and incidents
Understanding security requirements, including privacy 
and cybersecurity, vulnerabilities and threats, in line with
business requirements and impact
Managing user identities and authorizations in a 
standardized manner
Testing security regularly 

# I A R R R C/I

## Procurement and

contracts
Acquiring and maintaining I&T resources that respond to 
the delivery strategy, establishing an integrated and
standardized IT infrastructure, and reducing IT
procurement risk
Obtaining professional legal and contractual advice 
Deﬁning procurement procedures and standards 
Procuring requested hardware, software and services in 
line with deﬁned procedures

# I I C A/R C C

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

77

# A P P E N DIX  A

# E X A M P LE  DE C ISIO N  M A TR IX

3
15 IT m anagem ent includes all roles w ithin the IT function at a m anagem ent level.
Figure A.1 — Exam ple D ecision M atrix (cont.)

## Decision Topic Scope

Responsible, A ccountable,
C onsulted, Inform ed (RA C I)
Executive C om m ittee

## I& T G overnance Board

Enterprise Risk C om m ittee
Portfolio M anager
Steering (Program s/Projects) C om m ittee
IT M anagem ent 15
3
Business Process O w ners
Em ployees
I&T compliance  Identifying all applicable laws, regulations and contracts;
deﬁning the corresponding level of I&T compliance; and
optimizing IT processes to reduce the risk of
noncompliance
Identifying legal, regulatory and contractual requirements 
related to I&T
Assessing the impact of compliance requirements 
Monitoring and reporting on compliance with these 
requirements

# C/I A C A/R C C/I

## Personal Copy of Andrew Hana (ISACA ID: 1571067)

# C O B IT ® 2019 IM P LE M E N T A TIO N  GU IDE

P age intentionally left blank
78

## Personal Copy of Andrew Hana (ISACA ID: 1571067)