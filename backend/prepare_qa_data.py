import os
import json

CONVERTED_DIR = os.path.join(os.path.dirname(__file__), 'converted')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'qa_data.json')

# Mapping from file id to human-readable question and metadata, based on Exoplanet_explorer.py
QUESTION_MAP = {
    'q1_planets_by_hemisphere': {
        'question': 'How many planets are there per discovery method?',
        'metadata': {'topic': 'discovery method', 'type': 'count'}
    },
    'q2_planets_avg_temp_discovery_method': {
        'question': 'What is the average planet temperature per discovery method?',
        'metadata': {'topic': 'temperature', 'type': 'average'}
    },
    'q3_planets_max_temp': {
        'question': 'What is the maximum planet equilibrium temperature?',
        'metadata': {'topic': 'temperature', 'type': 'max'}
    },
    'q4_controversial_vs_confirmed_planets': {
        'question': 'How many controversial vs confirmed planets are there?',
        'metadata': {'topic': 'controversy', 'type': 'count'}
    },
    'q5_avg_metallicity_by_discovery': {
        'question': 'What is the average star metallicity by discovery method?',
        'metadata': {'topic': 'metallicity', 'type': 'average'}
    },
    'q6_planets_by_hemisphere_count': {
        'question': 'How many planets are in the northern vs southern sky?',
        'metadata': {'topic': 'hemisphere', 'type': 'count'}
    },
    'q7_hemisphere_pie_data': {
        'question': 'Pie chart data for planets by hemisphere (north vs south)',
        'metadata': {'topic': 'hemisphere', 'type': 'pie chart'}
    },
    'q8_hottest_high_metallicity_planets': {
        'question': 'What are the hottest planets with high metallicity stars?',
        'metadata': {'topic': 'temperature', 'type': 'top', 'filter': 'high metallicity'}
    },
    'q9_non_zero_orbital_axis_planets': {
        'question': 'Are there planets with non-zero orbital axis?',
        'metadata': {'topic': 'orbital axis', 'type': 'filter'}
    },
    'q10_planets_by_sky_quadrant': {
        'question': 'How many planets are there by sky quadrant?',
        'metadata': {'topic': 'sky quadrant', 'type': 'count'}
    },
    'q11_stddev_temp_by_discovery': {
        'question': 'What is the standard deviation of planet temperatures by discovery method?',
        'metadata': {'topic': 'temperature', 'type': 'stddev'}
    },
    'q12_planets_above_avg_temp': {
        'question': 'Which planets have temperature above the average?',
        'metadata': {'topic': 'temperature', 'type': 'filter', 'filter': 'above average'}
    },
    'q13_methods_metal_rich_planets': {
        'question': 'Which discovery methods have planets orbiting metal-rich stars (> 0.2 dex)?',
        'metadata': {'topic': 'metallicity', 'type': 'count', 'filter': 'metal-rich'}
    },
    'q14_coolest_transit_planets': {
        'question': 'What are the coolest 5 planets discovered via Transit method?',
        'metadata': {'topic': 'temperature', 'type': 'top', 'filter': 'coolest, transit'}
    },
    'q15_avg_temp_metallicity_by_hemisphere': {
        'question': 'What is the average temperature and metallicity by hemisphere?',
        'metadata': {'topic': 'hemisphere', 'type': 'average'}
    },
    'q16_controversial_by_hemisphere': {
        'question': 'What is the count of controversial planets by hemisphere?',
        'metadata': {'topic': 'controversy', 'type': 'count', 'by': 'hemisphere'}
    },
    'q17_extreme_orbital_axis_planets': {
        'question': 'Which are the most extreme orbital axis planets?',
        'metadata': {'topic': 'orbital axis', 'type': 'top'}
    },
    'q18_avg_by_quadrant': {
        'question': 'What are the average values per quadrant of the sky (RA + DEC)?',
        'metadata': {'topic': 'quadrant', 'type': 'average'}
    },
    'q19_discovery_with_controversy_and_confirmed': {
        'question': 'Which discovery methods have both confirmed and controversial planets?',
        'metadata': {'topic': 'discovery method', 'type': 'filter', 'filter': 'controversy'}
    },
    'q20_temp_percentiles_deciles': {
        'question': 'What are the temperature percentiles (deciles)?',
        'metadata': {'topic': 'temperature', 'type': 'percentile'}
    },
    'q21_avg_orbital_axis_by_method': {
        'question': 'What is the average orbital axis for planets discovered via each discovery method?',
        'metadata': {'topic': 'orbital axis', 'type': 'average'}
    },
    'q22_unique_discovery_methods_count': {
        'question': 'How many unique discovery methods are there in the dataset?',
        'metadata': {'topic': 'discovery method', 'type': 'count', 'unique': True}
    },
    'q23_avg_temp_by_hemisphere': {
        'question': 'Which declination hemisphere (North/South) has the higher average planet equilibrium temperature?',
        'metadata': {'topic': 'hemisphere', 'type': 'average', 'compare': 'north vs south'}
    },
    'q24_stddev_orbital_axis_by_method': {
        'question': 'What is the standard deviation of orbital axis for each discovery method?',
        'metadata': {'topic': 'orbital axis', 'type': 'stddev'}
    },
    'q25_high_metallicity_planets_count': {
        'question': 'How many planets have star metallicity greater than 0.05?',
        'metadata': {'topic': 'metallicity', 'type': 'count', 'filter': 'high metallicity'}
    },
    'q26_controversial_planets_by_method': {
        'question': 'Which discovery method has the most controversial planets?',
        'metadata': {'topic': 'controversy', 'type': 'count', 'by': 'discovery method'}
    },
    'q27_max_min_planet_temp': {
        'question': 'What is the max and min equilibrium temperature recorded in the dataset?',
        'metadata': {'topic': 'temperature', 'type': 'minmax'}
    },
    'q28_temp_bins_count': {
        'question': 'How many planets fall into each 500K temperature bin?',
        'metadata': {'topic': 'temperature', 'type': 'bin'}
    },
    'q29_top3_hemisphere_method_combos': {
        'question': 'What are the top 3 most common combinations of hemisphere and discovery method?',
        'metadata': {'topic': 'hemisphere+discovery method', 'type': 'top'}
    },
    'q30_discovery_method_percentages': {
        'question': 'What percentage of planets are discovered using each method?',
        'metadata': {'topic': 'discovery method', 'type': 'percentage'}
    },
    'q31_orbital_axis_type_percentages': {
        'question': 'What percentage of planets have zero vs non-zero orbital axis?',
        'metadata': {'topic': 'orbital axis', 'type': 'percentage'}
    },
    'q32_avg_temp_below_median_metallicity': {
        'question': 'What is the average temperature of planets with below-median metallicity?',
        'metadata': {'topic': 'temperature', 'type': 'average', 'filter': 'below median metallicity'}
    },
    'q33_median_orbital_axis_north': {
        'question': 'What is the median orbital axis for planets in the northern hemisphere?',
        'metadata': {'topic': 'orbital axis', 'type': 'median', 'hemisphere': 'north'}
    },
}

def load_json_lines(filepath):
    with open(filepath, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def main():
    qa_entries = []
    for fname in os.listdir(CONVERTED_DIR):
        if not fname.endswith('.json'):
            continue
        file_id = fname.replace('.json', '')
        question_info = QUESTION_MAP.get(file_id, None)
        if not question_info:
            question = f"What is the answer to {file_id.replace('_', ' ')}?"
            metadata = {"source_file": fname}
        else:
            question = question_info['question']
            metadata = question_info['metadata']
            metadata['source_file'] = fname
        # Load and serialize answer
        file_path = os.path.join(CONVERTED_DIR, fname)
        try:
            answer_data = load_json_lines(file_path)
            if len(answer_data) == 1:
                answer = json.dumps(answer_data[0])
            else:
                answer = json.dumps(answer_data)
        except Exception as e:
            answer = f"[Error loading answer: {e}]"
        qa_entries.append({
            "id": file_id,
            "question": question,
            "answer": answer,
            "metadata": metadata
        })
    # Write to output file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(qa_entries, f, indent=2)
    print(f"Wrote {len(qa_entries)} Q&A entries to {OUTPUT_FILE}")

if __name__ == "__main__":
    main() 