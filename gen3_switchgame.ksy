meta:
  id: miidata_swi
  endian: le
seq:
  - id: mii_id
    type: u1
    repeat: expr
    repeat-expr: 16
    doc: Mii ID. An identifier used to save Miis in most games.
  - id: mii_name
    type: str
    size: 22
    encoding: utf-16le
    doc: Mii name. Can be up to 10 characters long. Different from the Mii name that appears in Super Smash Bros. Ultimate - in that game, this is never seen.
  - id: font_region
    type: u1
    doc: Font region. 0 = USA + PAL + JPN, 1 = CHN, 2 = KOR, 3 = TWN.
  - id: favorite_color
    type: u1
    doc: Favorite color. Ranges from 0 to 11.
  - id: gender
    type: u1
    doc: Mii gender. 0 = male, 1 = female.
  - id: body_height
    type: u1
    doc: Body height. Ranges from 0 to 127, short to tall.
  - id: body_weight
    type: u1
    doc: Body weight. Ranges from 0 to 127, small to large.
  - id: special_type
    type: u1
    doc: Toggle if the Mii is a Special Mii. Completely unused functionality. Does not allow editing the Mii, or using the Mii in games.
  - id: region_move
    type: u1
    doc: Currently unknown.
  - id: face_type
    type: u1
    doc: Face shape. Ranges from 0 to 11. Not ordered the same as visible in editor.
  - id: face_color
    type: u1
    doc: Skin color. Ranges from 0 to 9. Not ordered the same as visible in editor.
  - id: face_wrinkles
    type: u1
    doc: Face wrinkles. Ranges from 0 to 11.
  - id: face_makeup
    type: u1
    doc: Face makeup. Ranges from 0 to 11.
  - id: hair_type
    type: u1
    doc: Hair type. Ranges from 0 to 131. Not ordered the same as visible in editor.
  - id: hair_color
    type: u1
    doc: Hair color. Ranges from 0 to 99. Not ordered the same as visible in editor.
  - id: hair_flip
    type: u1
    doc: Flip hair. 0 = no, 1 = yes.
  - id: eye_type
    type: u1
    doc: Eye type. Ranges from 0 to 59. Not ordered the same as visible in editor.
  - id: eye_color
    type: u1
    doc: Eye color. Ranges from 0 to 99. Not ordered the same as visible in editor.
  - id: eye_size
    type: u1
    doc: Eye size. Ranges from 0 to 7, small to large.
  - id: eye_stretch
    type: u1
    doc: Eye stretch. Ranges from 0 to 6, small to large.
  - id: eye_rotation
    type: u1
    doc: Eye rotation. Ranges from 0 to 7, down to up. Note that some eye types have a default rotation.
  - id: eye_horizontal
    type: u1
    doc: Eye X (horizontal) distance. Ranges from 0 to 12, close to far.
  - id: eye_vertical
    type: u1
    doc: Eye Y (vertical) position. Ranges from 18 to 0, low to high.
  - id: eyebrow_type
    type: u1
    doc: Eyebrow type. Ranges from 0 to 23. Not ordered the same as visible in editor.
  - id: eyebrow_color
    type: u1
    doc: Eyebrow color. Ranges from 0 to 99. Not ordered the same as visible in editor.
  - id: eyebrow_size
    type: u1
    doc: Eyebrow size. Ranges from 0 to 8, small to large.
  - id: eyebrow_stretch
    type: u1
    doc: Eyebrow stretch. Ranges from 0 to 6, small to large.
  - id: eyebrow_rotation
    type: u1
    doc: Eyebrow rotation. Ranges from 0 to 11, down to up. Note that some eyebrow types have a default rotation.
  - id: eyebrow_horizontal
    type: u1
    doc: Eyebrow X (horizontal) distance. Ranges from 0 to 12, close to far.
  - id: eyebrow_vertical
    type: u1
    doc: Eyebrow Y (vertical) distance. Ranges from 18 to 3, low to high.
  - id: nose_type
    type: u1
    doc: Nose type. Ranges from 0 to 17. Not ordered the same as visible in editor.
  - id: nose_size
    type: u1
    doc: Nose size. Ranges from 0 to 8, small to large.
  - id: nose_vertical
    type: u1
    doc: Nose Y (vertical) position. Ranges from 18 to 0, low to high.
  - id: mouth_type
    type: u1
    doc: Mouth type. Ranges from 0 to 35. Not ordered the same as visible in editor.
  - id: mouth_color
    type: u1
    doc: Mouth color. The default colors are ordered the same as visible in editor, ranging from 19 to 23. The custom colors are not and range from 0 to 99.
  - id: mouth_size
    type: u1
    doc: Mouth size. Ranges from 0 to 8, small to large.
  - id: mouth_stretch
    type: u1
    doc: Mouth stretch. Ranges from 0 to 6, small to large.
  - id: mouth_vertical
    type: u1
    doc: Mouth Y (vertical) position. Ranges from 18 to 0, low to high.
  - id: facial_hair_color
    type: u1
    doc: Facial hair color. Ranges from 0 to 99. Not ordered the same as visible in editor.
  - id: facial_hair_beard
    type: u1
    doc: Beard type. Ranges from 0 to 5.
  - id: facial_hair_mustache
    type: u1
    doc: Mustache type. Ranges from 0 to 5.
  - id: facial_hair_size
    type: u1
    doc: Mustache size. Ranges from 0 to 8, small to large.
  - id: facial_hair_vertical
    type: u1
    doc: Mustache Y (vertical) position. Ranges from 16 to 0, low to high.
  - id: glasses_type
    type: u1
    doc: Glasses type. Ranges from 0 to 19. Not ordered the same as visible in editor.
  - id: glasses_color
    type: u1
    doc: Glasses color. Ranges from 0 to 99. Not ordered the same as visible in editor.
  - id: glasses_size
    type: u1
    doc: Glasses size. Ranges from 0 to 7, small to large.
  - id: glasses_vertical
    type: u1
    doc: Glasses Y (vertical) position. Ranges from 20 to 0, low to high.
  - id: mole_enable
    type: u1
    doc: Enable mole. 0 = no, 1 = yes.
  - id: mole_size
    type: u1
    doc: Mole size. Ranges from 0 to 8, small to large.
  - id: mole_horizontal
    type: u1
    doc: Mole X (horizontal) position. Ranges from 0 to 16, left to right.
  - id: mole_vertical
    type: u1
    doc: Mole Y (vertical) position. Ranges from 30 to 0, low to high.
  - id: always_zero
    type: u1
    doc: This value is always set to 0. The Switch does properly document it, though, so it may end up used in some update... but most likely, it will always remain zero.