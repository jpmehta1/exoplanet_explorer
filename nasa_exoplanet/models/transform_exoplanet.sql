WITH base AS (

    SELECT
        RA AS right_ascension_deg,
        DEC AS declination_deg,
        PL_EQT AS planet_eq_temperature_k,
        COALESCE(ST_MET, AVG(ST_MET) OVER()) AS star_metallicity_dex,
        DISCOVERYMETHOD AS discovery_method,
        COALESCE(PL_CONTROV_FLAG, 0) AS controversial_flag,
        PL_ORBSMAXLIM AS orbital_axis_limit

    FROM PSCOMPPARS

    WHERE PL_EQT IS NOT NULL

)

SELECT * FROM base

