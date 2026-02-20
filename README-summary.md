## Smart Summary Feature

The system now includes intelligent content summarization and importance classification:

### Importance Levels
- 🔴 **High Priority**: New product launches, major breakthroughs, industry standards
- 🟡 **Medium Priority**: Product updates, conference news, research papers  
- 🟢 **Low Priority**: General news, company updates, routine announcements

### Automatic Summarization
- Extracts key points from articles
- Identifies technical terms and innovations
- Generates concise Chinese summaries
- Filters out low-quality or duplicate content

### Configuration
The `rss_config.json` file now includes:
- `enable_summary`: Toggle smart summarization (default: true)
- `importance_threshold`: Minimum importance level to notify (0-2, where 0=high, 2=low)
- `summary_length`: Maximum summary length in characters (default: 200)

This ensures you receive only the most relevant information with clear priority indicators.