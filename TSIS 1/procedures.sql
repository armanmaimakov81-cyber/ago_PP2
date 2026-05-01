DROP FUNCTION IF EXISTS search_contacts(TEXT);

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT,name TEXT,email TEXT,phone TEXT) AS $$
BEGIN
RETURN QUERY
SELECT 
c.id,
c.name,
c.email::TEXT,
COALESCE(p.phone::TEXT,'') AS phone
FROM contacts c
LEFT JOIN phones p ON c.id=p.contact_id
WHERE 
c.name ILIKE '%'||p_query||'%'
OR c.email ILIKE '%'||p_query||'%'
OR EXISTS (
    SELECT 1 FROM phones p2
    WHERE p2.contact_id=c.id
    AND p2.phone LIKE '%'||p_query||'%'
);
END;
$$ LANGUAGE plpgsql;
