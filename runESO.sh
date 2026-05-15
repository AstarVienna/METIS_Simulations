
#!/usr/bin/env bash
# Main orchestration script for running METIS simulation blocks
# Provides flexible execution modes: full run, partial run, single block, or small dataset
set -Eeuo pipefail # Exit on error, undefined vars, and pipe failures

# Get the absolute path to the directory containing this script
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# Define the directory where all simulation block Python scripts are located
BLOCK_DIR="${SCRIPT_DIR}/simulationBlocks"

# Set default environment variables for simulation configuration
# Users can override these by exporting them before running this script
export MSIM_YAML_DIR="${MSIM_YAML_DIR:-YAML/ESO}" # YAML configuration directory
export MSIM_NCORES="${MSIM_NCORES:-4}" # Number of CPU cores to use
export DEFAULT_IRDB_LOCATION="${DEFAULT_IRDB_LOCATION:-inst_pkgs}" # IRDB instrument data location
export MSIM_OUTDIR="${MSIM_OUTDIR:-output}" # Output directory for simulation results

# Define the complete list of simulation blocks in execution order
DEFAULT_BLOCKS=(
	imgLM   # Imaging mode - L band
	imgN    # Imaging mode - N band
	lssLM   # Long-slit spectroscopy - L band
	lssN    # Long-slit spectroscopy - N band
	ifu     # Integral Field Unit mode
	calib   # Calibration data
	hciRavcLM   # High-contrast imaging with RAVC - L band
	hciAppLm    # High-contrast imaging with app - L band
	hciRavcIfu  # High-contrast imaging with RAVC - IFU
)

# Initialize variables for command-line options
PYTHON_BIN="${PYTHON_BIN:-python}" # Python executable (can be overridden by user)
SMALL_MODE=false # Flag to enable small dataset mode
FROM_BLOCK=""    # Block name to start execution from
declare -a ONLY_BLOCKS=() # Array of specific blocks to run

# Print usage information and available options
usage() {
	cat <<'EOF'
Usage: ./runESO.sh [options]

Options:
	-p, --python <bin>    Python executable (default: python in PATH)
			--small           Run all blocks with --small flag and use small dataset
			--from <block>    Start execution from specified block to end
			--only <block>    Run only specified block(s) (can be repeated)
			--list            Print available blocks and exit
	-h, --help            Display this help message and exit

Examples:
	./runESO.sh                        # Run all blocks in default sequence
	./runESO.sh --only imgLM           # Execute only the imgLM block
	./runESO.sh --from lssN            # Execute from lssN block onwards
	./runESO.sh --small                # Run all blocks with small dataset
	./runESO.sh --only imgLM --only ifu  # Execute specific blocks in order
	./runESO.sh --from lssN --small    # Continue from lssN with small dataset
EOF
}

# Check if a given block name exists in the DEFAULT_BLOCKS array
contains_block() {
	local target="$1" # Block name to search for
	local block      # Current block in iteration
	for block in "${DEFAULT_BLOCKS[@]}"; do
		if [[ "$block" == "$target" ]]; then
			return 0 # Block found
		fi
	done
	return 1 # Block not found
}

# Print available blocks to help users understand valid block names
print_available_blocks() {
	echo "Available blocks:" >&2
	printf '  %s\n' "${DEFAULT_BLOCKS[@]}" >&2
}

# Parse command-line arguments with validation
while [[ $# -gt 0 ]]; do
	case "$1" in
		-p|--python)
			# Check if value is provided for --python
			if [[ $# -lt 2 ]]; then
				echo "Error: --python requires an argument" >&2
				usage >&2
				exit 2
			fi
			PYTHON_BIN="$2" # Store the Python executable path
			shift 2 # Move to next argument pair
			;;
		--small)
			SMALL_MODE=true # Enable small dataset mode
			shift # Move to next argument
			;;
		--from)
			# Check if value is provided for --from
			if [[ $# -lt 2 ]]; then
				echo "Error: --from requires a block name argument" >&2
				usage >&2
				exit 2
			fi
			FROM_BLOCK="$2" # Store the starting block name
			shift 2 # Move to next argument pair
			;;
		--only)
			# Check if value is provided for --only
			if [[ $# -lt 2 ]]; then
				echo "Error: --only requires a block name argument" >&2
				usage >&2
				exit 2
			fi
			ONLY_BLOCKS+=("$2") # Add block to execution list
			shift 2 # Move to next argument pair
			;;
		--list)
			printf '%s\n' "${DEFAULT_BLOCKS[@]}" # Print block list and exit
			exit 0
			;;
		-h|--help)
			usage # Print help message and exit
			exit 0
			;;
		*)
			echo "Error: Unknown option: $1" >&2 # Report unknown option
			usage >&2 # Show usage information
			exit 2
			;;
	esac
done


# Verify simulation block directory exists
if [[ ! -d "${BLOCK_DIR}" ]]; then
	echo "Error: Cannot find simulation block directory: ${BLOCK_DIR}" >&2
	exit 1
fi

# Verify Python executable exists and is executable
if ! command -v "${PYTHON_BIN}" &> /dev/null; then
	echo "Error: Python executable not found or not in PATH: ${PYTHON_BIN}" >&2
	exit 1
fi

# Build the list of blocks to execute based on command-line options
declare -a RUN_BLOCKS=()
if [[ ${#ONLY_BLOCKS[@]} -gt 0 ]]; then
	# User specified specific blocks with --only
	for block in "${ONLY_BLOCKS[@]}"; do
		# Validate each block name exists in the DEFAULT_BLOCKS array
		if ! contains_block "$block"; then
			echo "Error: Unknown block for --only: $block" >&2 # Report invalid block
			print_available_blocks # Show list of valid blocks
			exit 2
		fi
		RUN_BLOCKS+=("$block") # Add validated block to execution list
	done
else
	# No --only specified, use all default blocks
	RUN_BLOCKS=("${DEFAULT_BLOCKS[@]}")
fi

# Handle --from option to start execution from a specific block
if [[ -n "$FROM_BLOCK" ]]; then
	# Verify --from is not combined with --only (conflicting options)
	if [[ ${#ONLY_BLOCKS[@]} -gt 0 ]]; then
		echo "Error: --from cannot be combined with --only" >&2
		exit 2
	fi

	# Find the starting block and slice array from that point
	found=false # Track if starting block was found
	declare -a sliced=() # Array to hold blocks from starting point onwards
	for block in "${RUN_BLOCKS[@]}"; do
		# Check if current block matches the starting block
		if [[ "$block" == "$FROM_BLOCK" ]]; then
			found=true # Mark that we found the starting block
		fi
		# Add block to sliced array once starting block is found
		if [[ "$found" == true ]]; then
			sliced+=("$block")
		fi
	done

	# Verify the starting block exists in the sequence
	if [[ "$found" != true ]]; then
		echo "Error: Unknown block for --from: $FROM_BLOCK" >&2 # Report invalid starting block
		print_available_blocks # Show list of valid blocks
		exit 2
	fi

	RUN_BLOCKS=("${sliced[@]}") # Update RUN_BLOCKS to execute from starting point
fi

# Verify all simulation block files exist before execution begins
echo "[INFO] Verifying simulation block files..." >&2
for block in "${RUN_BLOCKS[@]}"; do
	block_file="${BLOCK_DIR}/${block}.py" # Construct full path to block script
	if [[ ! -f "$block_file" ]]; then
		# Report missing block file
		echo "Error: Block file not found: $block_file" >&2
		exit 1
	fi
done


# Handle small dataset mode by setting output directory and preserving original value
if [[ "$SMALL_MODE" == true ]]; then
	# Save the original METIS_ODIR value (or mark as unset)
	original_metis_odir="${METIS_ODIR-__UNSET__}"
	# Override output directory for small dataset runs
	export METIS_ODIR="Small/"
	# Set trap to restore original METIS_ODIR value when script exits
	trap 'if [[ "$original_metis_odir" == "__UNSET__" ]]; then unset METIS_ODIR; else export METIS_ODIR="$original_metis_odir"; fi' EXIT
fi

# Initialize error tracking and timing variables
current_block="startup" # Track current block for error reporting
trap 'echo "[ERROR] block=${current_block} command=${BASH_COMMAND} line=${LINENO}" >&2' ERR # Report errors with context

# Get total count of blocks to execute and initialize progress counter
total=${#RUN_BLOCKS[@]} # Total number of blocks to run
index=0 # Current block index

# Print execution summary before starting
echo "[INFO] Starting simulation blocks: ${RUN_BLOCKS[*]}"
echo "[INFO] Python executable: ${PYTHON_BIN}"
echo "[INFO] Configuration: MSIM_YAML_DIR=${MSIM_YAML_DIR}, MSIM_NCORES=${MSIM_NCORES}, MSIM_OUTDIR=${MSIM_OUTDIR}"
if [[ "$SMALL_MODE" == true ]]; then
	echo "[INFO] Running in SMALL mode with output directory: ${METIS_ODIR}"
fi

# Execute each simulation block in sequence
for block in "${RUN_BLOCKS[@]}"; do
	index=$((index + 1)) # Increment progress counter
	current_block="$block" # Update current block for error tracking
	start_ts=$(date +%s) # Record block start time

	# Create GitHub Actions log group for better CI visibility
	if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
		echo "::group::[$index/$total] ${block}" # Start collapsible group in CI logs
	fi

	# Print block execution info
	echo "[INFO] [$index/$total] Running ${block}"
	# Construct command array with Python executable and block script
	cmd=("${PYTHON_BIN}" "${BLOCK_DIR}/${block}.py")
	# Add --small flag if running in small dataset mode
	if [[ "$SMALL_MODE" == true ]]; then
		cmd+=("--small")
	fi
	# Execute the block script
	"${cmd[@]}"

	# Calculate and report block execution time
	end_ts=$(date +%s) # Record block end time
	elapsed=$((end_ts - start_ts)) # Calculate elapsed seconds
	echo "[INFO] [$index/$total] Finished ${block} in ${elapsed}s"

	# Close GitHub Actions log group
	if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
		echo "::endgroup::" # End collapsible group in CI logs
	fi
done

# Print final completion summary
echo "[INFO] Completed ${total} simulation blocks"
