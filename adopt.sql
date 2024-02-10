DROP DATABASE IF EXISTS adopt WITH (FORCE); 

CREATE DATABASE adopt;

\c adopt

-- INSERT INTO pets
--   (name, species, age, notes, photo_url, available)
-- VALUES
--   ('Cam', 'Dog', 3, 'He''s a good puppo, too', 'https://upload.wikimedia.org/wikipedia/commons/a/a1/Airedale-terrier-charles14m.jpg', True);