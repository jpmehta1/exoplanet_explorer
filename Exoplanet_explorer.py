#!/usr/bin/env python
# coding: utf-8

# In[195]:


from sqlalchemy import create_engine
import pandas as pd
import snowflake.connector
import matplotlib.pyplot as plt
import pickle
# connector 
conn = snowflake.connector.connect(
    user = "MEHTAJEETPARESH",
    password = "Jeetmehta12345",
    account = "xo45240.us-central1.gcp",
    role = 'NASA_ROLE',
    warehouse = "COMPUTE_WH",
    database = "NASA_PROJECT",
    schema = "EXOPLANET_DATA"
)

cursor = conn.cursor()
cursor.execute("USE DATABASE NASA_PROJECT;")
cursor.execute("USE SCHEMA EXOPLANET_DATA;")


# In[191]:


# checking original dataset
df = pd.read_sql("""
            SELECT *
            FROM PSCOMPPARS
            LIMIT 5
            """, conn)


# In[193]:


# checking transformed dataset
transformed_df = pd.read_sql("""
SELECT * FROM TRANSFORM_EXOPLANET LIMIT 5
""", conn)

transformed_df.head()


# ## ANALYSIS STARTS HERE ##

# In[196]:


# 1. number of planets per discovery method ordered by count of number of planets
q1 = pd.read_sql("""
SELECT discovery_method, COUNT(*) AS num_planets
FROM TRANSFORM_EXOPLANET
GROUP BY discovery_method
ORDER BY num_planets DESC
""", conn)

with open("answers/q1_planets_by_hemisphere.pkl", "wb") as f:
    pickle.dump(q1, f)


# In[198]:


# 2. average planet temperature per discovery method
q2 = pd.read_sql("""
SELECT discovery_method, AVG(planet_eq_temperature_k) AS avg_planet_eq_temp_k
FROM TRANSFORM_EXOPLANET
GROUP BY discovery_method
ORDER BY avg_planet_eq_temp_k DESC
""", conn)

with open("answers/q2_planets_avg_temp_discovery_method.pkl", "wb") as f:
    pickle.dump(q2, f)


# In[199]:


# 3. planet with max temperature
q3 = pd.read_sql("""
SELECT MAX(planet_eq_temperature_k) AS max_temp_k
FROM TRANSFORM_EXOPLANET
""", conn)

with open("answers/q3_planets_max_temp.pkl", "wb") as f:
    pickle.dump(q3, f)


# In[200]:


# 4. number of controversial vs confirmed planets
q4 = pd.read_sql("""
SELECT controversial_flag, COUNT(*) AS count
FROM TRANSFORM_EXOPLANET
GROUP BY controversial_flag
""", conn)

with open("answers/q4_controversial_vs_confirmed_planets.pkl", "wb") as f:
    pickle.dump(q4, f)


# In[105]:


# 5. average metallicity by discovery method
q5 = pd.read_sql("""
SELECT discovery_method, AVG(STAR_METALLICITY_DEX) AS avg_metallicity_dex
FROM TRANSFORM_EXOPLANET
GROUP BY discovery_method
ORDER BY avg_metallicity_dex DESC
""", conn)

with open("answers/q5_avg_metallicity_by_discovery.pkl", "wb") as f:
    pickle.dump(q5, f)


# In[116]:


# 6. count of planets in northern vs southern sky
q6 = pd.read_sql("""
SELECT
    CASE WHEN declination_deg >= 0 THEN 'North' ELSE 'South' END AS hemisphere,
    COUNT(*) AS num_planets
FROM TRANSFORM_EXOPLANET
GROUP BY hemisphere
""", conn)

with open("answers/q6_planets_by_hemisphere_count.pkl", "wb") as f:
    pickle.dump(q6, f)


# In[122]:


# 7. pie chart for the count of planets in northern vs southern sky
import matplotlib.pyplot as plt
q7 = q6.copy()
q7.set_index('HEMISPHERE')['NUM_PLANETS'].plot.pie(
    autopct='%1.1f%%',
    figsize=(6, 6),
    ylabel=''
)
plt.title('Planets by Hemisphere (North vs South)')
with open("answers/q7_hemisphere_pie_data.pkl", "wb") as f:
    pickle.dump(q7, f)


# In[109]:


# 8. hottest planets with high metallicity stars
q8 = pd.read_sql("""
SELECT *
FROM TRANSFORM_EXOPLANET 
WHERE star_metallicity_dex > 0.1
ORDER BY planet_eq_temperature_k DESC
LIMIT 10
""", conn)
with open("answers/q8_hottest_high_metallicity_planets.pkl", "wb") as f:
    pickle.dump(q8, f)


# In[111]:


# 9. Planets with non zero orbital axis -> none are,lol
q9 = pd.read_sql("""
SELECT *
FROM TRANSFORM_EXOPLANET 
WHERE ORBITAL_AXIS_LIMIT > 0.0
LIMIT 10
""", conn)
with open("answers/q9_non_zero_orbital_axis_planets.pkl", "wb") as f:
    pickle.dump(q9, f)


# In[114]:


# 10. Count of planets by quadrant (RA/DEC)
q10 = pd.read_sql("""
SELECT
    CASE
        WHEN RIGHT_ASCENSION_DEG > 180 AND declination_deg > 0 THEN 'Q1'
        WHEN RIGHT_ASCENSION_DEG <= 180 AND declination_deg > 0 THEN 'Q2'
        WHEN RIGHT_ASCENSION_DEG <= 180 AND declination_deg <= 0 THEN 'Q3'
        ELSE 'Q4'
    END AS sky_quadrant,
    COUNT(*) AS num_planets
FROM TRANSFORM_EXOPLANET
GROUP BY sky_quadrant
""", conn)
with open("answers/q10_planets_by_sky_quadrant.pkl", "wb") as f:
    pickle.dump(q10, f)


# In[130]:


# 11. Standard deviation of planet temperatures by discovery method
q11 = pd.read_sql("""
SELECT discovery_method, STDDEV(planet_eq_temperature_k) as stddev_planet_eq_temperature_k
FROM TRANSFORM_EXOPLANET
GROUP BY discovery_method 
ORDER BY stddev_planet_eq_temperature_k DESC
""",conn)
with open("answers/q11_stddev_temp_by_discovery.pkl", "wb") as f:
    pickle.dump(q11, f)


# In[132]:


# 12. Planets with temperature above the average temperature
q12 = pd.read_sql("""
SELECT *
FROM TRANSFORM_EXOPLANET
WHERE planet_eq_temperature_k > (SELECT AVG(planet_eq_temperature_k) FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET);
""",conn)
with open("answers/q12_planets_above_avg_temp.pkl", "wb") as f:
    pickle.dump(q12, f)


# In[135]:


# 13. Discovery methods with planets orbiting metal-rich stars (> 0.2 dex)
q13 = pd.read_sql("""
SELECT discovery_method, COUNT(*) AS count
FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET
WHERE star_metallicity_dex > 0.2
GROUP BY discovery_method
ORDER BY count DESC
""",conn)
with open("answers/q13_methods_metal_rich_planets.pkl", "wb") as f:
    pickle.dump(q13, f)



# In[136]:


# 14. Coolest 5 planets discovered via Transit method
q14 = pd.read_sql("""
SELECT *
FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET
WHERE discovery_method = 'Transit'
ORDER BY planet_eq_temperature_k ASC
LIMIT 5;
""",conn)
with open("answers/q14_coolest_transit_planets.pkl", "wb") as f:
    pickle.dump(q14, f)


# In[138]:


# 15. Average temperature and metallicity by hemisphere
q15 = pd.read_sql("""
SELECT
  CASE WHEN declination_deg >= 0 THEN 'North' ELSE 'South' END AS hemisphere,
  AVG(planet_eq_temperature_k) AS avg_temp,
  AVG(star_metallicity_dex) AS avg_metallicity
FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET
GROUP BY hemisphere;
""",conn)

with open("answers/q15_avg_temp_metallicity_by_hemisphere.pkl", "wb") as f:
    pickle.dump(q15, f)


# In[139]:


# 16. Count of controversial planets by hemisphere
q16 = pd.read_sql("""
SELECT
  CASE WHEN declination_deg >= 0 THEN 'North' ELSE 'South' END AS hemisphere,
  COUNT(*) AS controversial_count
FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET
WHERE controversial_flag = 1
GROUP BY hemisphere;
""",conn)
with open("answers/q16_controversial_by_hemisphere.pkl", "wb") as f:
    pickle.dump(q16, f)


# In[140]:


# 17. Most extreme orbital axis planets (top 5)
q17 = pd.read_sql("""
SELECT *
FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET
ORDER BY orbital_axis_limit DESC
LIMIT 5;
""",conn)
with open("answers/q17_extreme_orbital_axis_planets.pkl", "wb") as f:
    pickle.dump(q17, f)


# In[143]:


# 18. Average values per quadrant of the sky (RA + DEC)
q18 = pd.read_sql("""
SELECT
  CASE
    WHEN RIGHT_ASCENSION_DEG > 180 AND DECLINATION_DEG > 0 THEN 'Q1'
    WHEN RIGHT_ASCENSION_DEG <= 180 AND DECLINATION_DEG > 0 THEN 'Q2'
    WHEN RIGHT_ASCENSION_DEG <= 180 AND DECLINATION_DEG <= 0 THEN 'Q3'
    ELSE 'Q4'
  END AS quadrant,
  AVG(planet_eq_temperature_k) AS avg_temp,
  AVG(star_metallicity_dex) AS avg_metallicity
FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET
GROUP BY quadrant;
""",conn)
with open("answers/q18_avg_by_quadrant.pkl", "wb") as f:
    pickle.dump(q18, f)


# In[144]:


# 19. Discovery methods with both confirmed and controversial planets
q19 = pd.read_sql("""
SELECT discovery_method
FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET
GROUP BY discovery_method
HAVING COUNT(DISTINCT controversial_flag) > 1;
""",conn)
with open("answers/q19_discovery_with_controversy_and_confirmed.pkl", "wb") as f:
    pickle.dump(q19, f)


# In[147]:


# 20. Temperature percentiles (deciles)
q20 = pd.read_sql("""
SELECT decile,COUNT(*) AS count
FROM (
  SELECT
    NTILE(10) OVER (ORDER BY planet_eq_temperature_k) AS decile
  FROM TRANSFORM_EXOPLANET
  WHERE planet_eq_temperature_k IS NOT NULL
) AS sub
GROUP BY decile
ORDER BY decile;
""",conn)
with open("answers/q20_temp_percentiles_deciles.pkl", "wb") as f:
    pickle.dump(q20, f)


# In[149]:


# 21. Average orbital axis for planets discovered via each discovery method?
q21 = pd.read_sql("""
SELECT discovery_method , AVG(ORBITAL_AXIS_LIMIT) AS avg_orbital_axis
FROM EXOPLANET_DATA.TRANSFORM_EXOPLANET
GROUP BY discovery_method
""",conn)
with open("answers/q21_avg_orbital_axis_by_method.pkl", "wb") as f:
    pickle.dump(q21, f)


# In[150]:


# 22. How many unique discovery methods are there in the dataset?
q22 = pd.read_sql("""
SELECT COUNT(DISTINCT(DISCOVERY_METHOD)) AS count_discovery_method
FROM TRANSFORM_EXOPLANET
""",conn)
with open("answers/q22_unique_discovery_methods_count.pkl", "wb") as f:
    pickle.dump(q21, f)


# In[153]:


# 23. Which declination hemisphere (North/South) has the higher average planet equilibrium temperature?
q23 = pd.read_sql("""
SELECT hemisphere, AVG(planet_eq_temperature_k) AS avg_temp
       FROM (
           SELECT *, CASE WHEN declination_deg >= 0 THEN 'North' ELSE 'South' END AS hemisphere
           FROM TRANSFORM_EXOPLANET
       )
       GROUP BY hemisphere
""",conn)
with open("answers/q23_avg_temp_by_hemisphere.pkl", "wb") as f:
    pickle.dump(q23, f)


# In[154]:


# 24. What is the standard deviation of orbital axis for each discovery method?
q24 = pd.read_sql("""
SELECT discovery_method, STDDEV(orbital_axis_limit) AS stddev_orbital_axis
       FROM TRANSFORM_EXOPLANET
       GROUP BY discovery_method
""",conn)
with open("answers/q24_stddev_orbital_axis_by_method.pkl", "wb") as f:
    pickle.dump(q24, f)


# In[156]:


# 25. How many planets have star metallicity greater than 0.05?
q25 = pd.read_sql("""
SELECT COUNT(*) AS high_metallicity_planets
       FROM TRANSFORM_EXOPLANET
       WHERE star_metallicity_dex > 0.05
""",conn)
with open("answers/q25_high_metallicity_planets_count.pkl", "wb") as f:
    pickle.dump(q25, f)


# In[157]:


# 26. Which discovery method has the most controversial planets?
q26 = pd.read_sql("""
SELECT COUNT(*) AS high_metallicity_planets
       FROM TRANSFORM_EXOPLANET
       WHERE star_metallicity_dex > 0.05
""",conn)
with open("answers/q26_controversial_planets_by_method.pkl", "wb") as f:
    pickle.dump(q26, f)      


# In[158]:


# 27. What’s the max and min equilibrium temperature recorded in the dataset?
q27 = pd.read_sql("""
SELECT MAX(planet_eq_temperature_k) AS max_temp, MIN(planet_eq_temperature_k) AS min_temp
       FROM TRANSFORM_EXOPLANET
""",conn)
with open("answers/q27_max_min_planet_temp.pkl", "wb") as f:
    pickle.dump(q27, f)      
    


# In[159]:


#28. Group planets into bins of 500K based on equilibrium temperature and count how many fall into each bin.
q28 = pd.read_sql("""
SELECT FLOOR(planet_eq_temperature_k / 500) * 500 AS temp_bin_start,
              COUNT(*) AS count_in_bin
       FROM TRANSFORM_EXOPLANET
       WHERE planet_eq_temperature_k IS NOT NULL
       GROUP BY temp_bin_start
       ORDER BY temp_bin_start
""",conn)
with open("answers/q28_temp_bins_count.pkl", "wb") as f:
    pickle.dump(q28, f)
    


# In[160]:


#29. Find the top 3 most common combinations of hemisphere and discovery method
q29 = pd.read_sql("""
SELECT hemisphere, discovery_method, COUNT(*) AS count
       FROM (
           SELECT *, CASE WHEN declination_deg >= 0 THEN 'North' ELSE 'South' END AS hemisphere
           FROM TRANSFORM_EXOPLANET
       )
       GROUP BY hemisphere, discovery_method
       ORDER BY count DESC
       LIMIT 3
""",conn)
with open("answers/q29_top3_hemisphere_method_combos.pkl", "wb") as f:
    pickle.dump(q29, f)   


# In[161]:


#30. Calculate correlation between star metallicity and planet temperature. 
q30 = pd.read_sql("""
SELECT
         discovery_method,
         COUNT(*) * 100.0 / (SELECT COUNT(*) FROM TRANSFORM_EXOPLANET) AS percentage
       FROM TRANSFORM_EXOPLANET
       GROUP BY discovery_method
""",conn)
with open("answers/q30_discovery_method_percentages.pkl", "wb") as f:
    pickle.dump(q30, f)


# In[162]:


#31. What percentage of planets are discovered using Imaging vs others?
q31 = pd.read_sql("""
SELECT

         CASE WHEN orbital_axis_limit = 0 THEN 'Zero' ELSE 'Non-zero' END AS axis_type,
         COUNT(*) AS count
       FROM TRANSFORM_EXOPLANET
       GROUP BY axis_type
""",conn)
with open("answers/q31_orbital_axis_type_percentages.pkl", "wb") as f:
    pickle.dump(q31, f)


# In[ ]:


#32. Compare the count of planets with orbital axis 0 vs non-zero.
q32 = pd.read_sql("""
WITH median_metallicity AS (
         SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY star_metallicity_dex) AS median_val
         FROM TRANSFORM_EXOPLANET
         WHERE star_metallicity_dex IS NOT NULL
       )
       SELECT AVG(planet_eq_temperature_k) AS avg_temp
       FROM TRANSFORM_EXOPLANET, median_metallicity
       WHERE star_metallicity_dex < median_val
 """,conn)
with open("answers/q32_avg_temp_below_median_metallicity.pkl", "wb") as f:
    pickle.dump(q32, f)      
       


# In[166]:


#33. Are there planets with unusually high or low metallicity? Get 5 rows from each end of the metallicity range.
q33 = pd.read_sql("""
SELECT MEDIAN(orbital_axis_limit) AS median_orbital_axis
       FROM TRANSFORM_EXOPLANET
       WHERE declination_deg >= 0
""",conn)
with open("answers/q33_median_orbital_axis_north.pkl", "wb") as f:
    pickle.dump(q33, f)       
       



