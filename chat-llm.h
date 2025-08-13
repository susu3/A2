#ifndef __CHAT_LLM_H
#define __CHAT_LLM_H

#include "klist.h"
#include "khash.h"
#include "types.h"
#include <json-c/json.h>
#include <stdbool.h>

// Function declaration
const char* get_openai_token(void);

#define MAX_PROMPT_LENGTH 16384   //chat-llm.c中没有，afl-fuzz.c中也没有
#define EXAMPLES_PROMPT_LENGTH 400
#define HISTORY_PROMPT_LENGTH 1300
#define EXAMPLE_SEQUENCE_PROMPT_LENGTH 1700

#define TEMPLATE_CONSISTENCY_COUNT 5

// Maximum amount of retries for the state stall
#define STALL_RETRIES 2

// Maximum amount of tries to get the grammars
#define GRAMMAR_RETRIES 5

// Maximum amount
#define MESSAGE_TYPE_RETRIES 5

//Maximum amount of tries for an enrichment
#define ENRICHMENT_RETRIES 5

// Maximum number of messages to be added
#define MAX_ENRICHMENT_MESSAGE_TYPES 2

// Maximum number of messages to examine for addition
#define MAX_ENRICHMENT_CORPUS_SIZE 10

#define PCRE2_CODE_UNIT_WIDTH 8 // Characters are 8 bits
#include <pcre2.h>

// RFC Consistency Analysis Configuration
#define RFC_CONSISTENCY_RETRIES 3

// Data collection modes
typedef enum {
    COLLECT_DISABLED = 0,           // disable collection
    COLLECT_NEW_COVERAGE_ONLY = 1,  // only new coverage (hnb=2)
    COLLECT_WITH_SAMPLING = 2       // new coverage + no duplicate random sampling
} consistency_collect_mode_t;

// Optional: Structured data types for advanced processing
// (Currently unused but available for future extensions)

// Single request-response pair
typedef struct {
    char *request_hex;           // Request data (hex encoded for LLM processing)
    u32 request_len;             // Request length
    char *response_hex;          // Response data (hex encoded, NULL if no response)
    u32 response_len;            // Response length (0 if no response/timeout)
    // Note: response_time_us removed - not reliably available in current AFL-ICS implementation
} request_response_pair_t;

// Complete interaction record (simplified version, redundant fields removed)
typedef struct {
    u64 timestamp;               // Timestamp (for sorting and context)
    char *test_case_id;          // Test case ID (for traceability)
    u32 total_pairs;             // Total number of request-response pairs
    request_response_pair_t *pairs; // Array of request-response pairs
} interaction_record_t;

// Simplified data collection buffer
typedef struct {
    FILE *output_file;           // Current output file handle
    char *current_file_path;     // Current file path
    u32 current_record_id;       // Current record ID
} consistency_buffer_t;

// Init KLIST with JSON object
// #define __grammar_t_free(x)
// #define __rang_t_free(x)
// #define __khash_t_free(x) 
// KHASH_SET_INIT_STR(strSet);
// KLIST_INIT(gram, json_object *, __grammar_t_free)
// KLIST_INIT(rang, pcre2_code **, __rang_t_free)
// typedef struct
// {
//     int start;
//     int len;
//     int mutable;
// } range;

// typedef kvec_t(range) range_list;
// typedef kvec_t(khash_t(strSet)*) message_set_list;

// define one map to save pairs: {key: string, value: int}
// KHASH_MAP_INIT_STR(strMap, int)
// KHASH_MAP_INIT_STR(field_table, int);
// KHASH_INIT(consistency_table, const char *, khash_t(field_table) *, 1, kh_str_hash_func, kh_str_hash_equal);

// Function declarations
char *chat_with_llm(char *prompt, int tries, float temperature);
//char *construct_prompt_for_seeds(char *protocol_name, char **final_msg, char *seedfile_path, char *rfc_path);
char *construct_prompt_for_seeds_message(char *protocol_name, char **final_msg, const char *seedfile_path, char *rfc_path);
char *construct_prompt_for_seeds_sequence(char *protocol_name, char **final_msg, char *rfc_path);
char **extract_sequences(const char *llm_output, int *num_sequences);
char **extract_messages(const char *llm_output, int *num_messages);
void write_sequences_to_seeds(const char *seedfile_path, char **sequences, int num_sequences);
void write_messages_to_seeds(const char *seedfile_path, char **messages, int num_messages);
void extract_and_save_sequences(const char *llm_output, const char *output_dir);
void write_new_seeds(char *enriched_file, char *contents);
void cleanup_length_arrays(void);


// Protocol analysis functions
char *construct_prompt_for_message_grammar(const char *protocol_name, const char *spec_path);
char *construct_prompt_for_state_machine(const char *protocol_name, const char *spec_path);
void parse_and_save_message_grammar(const char *llm_response, const char *protocol_name, const char *output_dir);
void save_state_machine(const char *llm_response, const char *protocol_name, const char *output_dir);
//bool verify_protocol_analysis(const char *protocol_name, const char *output_dir, const char *spec_path, char **verification_result);
//bool improve_protocol_analysis(const char *protocol_name, const char *output_dir, const char *verification_json);
//bool verify_and_improve_protocol_analysis(const char *protocol_name, const char *output_dir, const char *spec_path);
bool verify_and_update_protocol_grammar(const char *protocol_name, const char *output_dir, const char *spec_path);
bool verify_and_update_protocol_state_machine(const char *protocol_name, const char *output_dir, const char *spec_path);


// Utility functions
//khash_t(strSet)* duplicate_hash(khash_t(strSet)* set);

// RFC Consistency Analysis Function Declarations
int init_rfc_consistency_analysis(const char *output_dir);
void cleanup_rfc_consistency_analysis(void);
void set_rfc_consistency_mode(consistency_collect_mode_t mode, unsigned int sampling_rate);
int collect_interaction_data(void *kl_messages_ptr, void *response_buf_ptr, 
                           unsigned int *response_bytes_ptr, unsigned int messages_sent_count);
int perform_rfc_consistency_analysis(const char *rfc_path, const char *protocol_name, const char *output_dir);
int should_collect_consistency_data(unsigned char has_new_bits_value);

// Helper function declarations
char *bytes_to_hex_string(const unsigned char *data, unsigned int length);
char *get_current_timestamp_string(void);
char *read_entire_file(const char *file_path);


#endif // __CHAT_LLM_H
