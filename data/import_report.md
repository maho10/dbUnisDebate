# Import report

- Records: **139**
- Verified: 49
- Types: universidad 119, escolar 4, independiente 16

## BLOCKING: duplicate codes (2)
Codes must be unique. Rename or merge these rows.
- row 73: `SODE SAH` — Sociedad de Debate San Antonio de Huamanga (—, no country); row 77: `SODESAH` — Sociedad de debate San Antonio de Huamanga (—, no country)
- row 126: `URL` — Universidad Rafael Landívar (Universidad Rafael Landívar, Guatemala); row 135: `URL` — Sociedad de Debate URL (Universidad Rafael Landívar, no country)

## BLOCKING: missing code (2)
These rows are skipped on MongoDB upload until they get a code.
- row 30: `(no code)` — Centro Universitario de Ciencias de la Salud (Centro Universitario de Ciencias de la Salud, México)
- row 139: `(no code)` — ? (Universidad Católica de la Santísima Concepción, no country)

## Likely duplicates (3)
Rows sharing a code, society acronym or society name. Merge them or confirm they are different.
- row 16: `CDUP` — Club de Debate de la Universidad de Panamá (Universidad de Panamá, Panamá)<br>row 110: `UP` — Club de Debate de la Universidad de Panamá (Universidad de Panamá, Panamá)
- row 73: `SODE SAH` — Sociedad de Debate San Antonio de Huamanga (—, no country)<br>row 77: `SODESAH` — Sociedad de debate San Antonio de Huamanga (—, no country)
- row 126: `URL` — Universidad Rafael Landívar (Universidad Rafael Landívar, Guatemala)<br>row 135: `URL` — Sociedad de Debate URL (Universidad Rafael Landívar, no country)

## Missing country (19)
- row 41: `IPA` — Instituto Panamericano (Instituto Panamericano, no country)
- row 43: `ISC` — Sociedad de Debate del Instituto Sagrado Corazón (Instituto Sagrado Corazón, no country)
- row 45: `JUD` — Jovenes Unidos por el Dialogo (—, no country)
- row 46: `LUD` — Liga Universitaria de Debate (—, no country)
- row 61: `SDU` — Sociedad de Debate Uniandina (—, no country)
- row 68: `SEDEVI` — seleccion debate vitacura (—, no country)
- row 73: `SODE SAH` — Sociedad de Debate San Antonio de Huamanga (—, no country)
- row 77: `SODESAH` — Sociedad de debate San Antonio de Huamanga (—, no country)
- row 78: `SODEUCH` — Sociedad de Debate de la Universidad de Chile (—, no country)
- row 80: `SODEZA` — sociedad de debate zarate (—, no country)
- row 84: `TRD` — Torneos regionales de debates (—, no country)
- row 118: `VD` — Verano en Debate (—, no country)
- row 122: `Comillas` — Universidad Pontificia Comillas (Universidad Pontificia Comillas, no country)
- row 123: `EUNEIZ` — Universidad Vitoria-Gasteiz (Universidad Vitoria-Gasteiz, no country)
- row 124: `UASD` — Universidad Autónoma de Santo Domingo (Universidad Autónoma de Santo Domingo, no country)
- row 125: `California` — California Polytechnic State University - San Luis Obispo (California Polytechnic State University - San Luis Obispo, no country)
- row 127: `UCBSP` — Universidad Católica Boliviana San Pablo (Universidad Católica Boliviana San Pablo, no country)
- row 135: `URL` — Sociedad de Debate URL (Universidad Rafael Landívar, no country)
- row 139: `(no code)` — ? (Universidad Católica de la Santísima Concepción, no country)

## Missing society name (1)
- row 139: `(no code)` — ? (Universidad Católica de la Santísima Concepción, no country)

## Institutions with several societies (info) (7)
Fine if they really are different societies; otherwise they are duplicates.
- Universidad de Panamá: `CDUP`, `UP`
- Universidad de Guadalajara: `CUCSH UDEG`, `SAUDG`
- Universidad Nacional Mayor de San Marcos: `ODSM`, `UNMSM`
- Universidad Nacional Autónoma de México: `PoCu`, `UNAM`
- Universidad Complutense de Madrid: `UCM`, `UCM-COM`
- Universidad Peruana de Ciencias Aplicadas: `SODEUPC`, `UPC`
- Universidad Rafael Landívar: `URL`, `URL`

## Country spellings (check for variants) (14)
- Brasil
- Chile
- Colombia
- Costa Rica
- Ecuador
- España
- Estados Unidos
- Guatemala
- México
- Panamá
- Perú
- Reino Unido
- Republica Dominicana
- Venezuela
