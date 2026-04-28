
#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BLOCK_DIR="${SCRIPT_DIR}/simulationBlocks"

export MSIM_YAML_DIR="${MSIM_YAML_DIR:-YAML/ESO}"
export MSIM_NCORES="${MSIM_NCORES:-4}"
export DEFAULT_IRDB_LOCATION="${DEFAULT_IRDB_LOCATION:-inst_pkgs}"
export MSIM_OUTDIR="${MSIM_OUTDIR:-output}"

DEFAULT_BLOCKS=(
	imgLM
	imgN
	lssLM
	lssN
	ifu
	calib
	hciRavcLM
	hciAppLm
	hciRavcIfu
)

PYTHON_BIN="${PYTHON_BIN:-python}"
SMALL_MODE=false
FROM_BLOCK=""
declare -a ONLY_BLOCKS=()

usage() {
	cat <<'EOF'
Usage: ./runESO.sh [options]

Options:
	-p, --python <bin>    Python executable (default: $PYTHON_BIN or python)
			--small           Run all blocks with --small and set METIS_ODIR to Small/
			--from <block>    Start from this block in the default sequence
			--only <block>    Run only one block (can be repeated)
			--list            Print default block sequence and exit
	-h, --help            Show this help message
EOF
}

contains_block() {
	local target="$1"
	local block
	for block in "${DEFAULT_BLOCKS[@]}"; do
		if [[ "$block" == "$target" ]]; then
			return 0
		fi
	done
	return 1
}

while [[ $# -gt 0 ]]; do
	case "$1" in
		-p|--python)
			PYTHON_BIN="$2"
			shift 2
			;;
		--small)
			SMALL_MODE=true
			shift
			;;
		--from)
			FROM_BLOCK="$2"
			shift 2
			;;
		--only)
			ONLY_BLOCKS+=("$2")
			shift 2
			;;
		--list)
			printf '%s\n' "${DEFAULT_BLOCKS[@]}"
			exit 0
			;;
		-h|--help)
			usage
			exit 0
			;;
		*)
			echo "Unknown option: $1" >&2
			usage >&2
			exit 2
			;;
	esac
done

if [[ ! -d "${BLOCK_DIR}" ]]; then
	echo "Cannot find simulation block directory: ${BLOCK_DIR}" >&2
	exit 1
fi

declare -a RUN_BLOCKS=()
if [[ ${#ONLY_BLOCKS[@]} -gt 0 ]]; then
	for block in "${ONLY_BLOCKS[@]}"; do
		if ! contains_block "$block"; then
			echo "Unknown block for --only: $block" >&2
			exit 2
		fi
		RUN_BLOCKS+=("$block")
	done
else
	RUN_BLOCKS=("${DEFAULT_BLOCKS[@]}")
fi

if [[ -n "$FROM_BLOCK" ]]; then
	if [[ ${#ONLY_BLOCKS[@]} -gt 0 ]]; then
		echo "--from cannot be combined with --only" >&2
		exit 2
	fi

	found=false
	declare -a sliced=()
	for block in "${RUN_BLOCKS[@]}"; do
		if [[ "$block" == "$FROM_BLOCK" ]]; then
			found=true
		fi
		if [[ "$found" == true ]]; then
			sliced+=("$block")
		fi
	done

	if [[ "$found" != true ]]; then
		echo "Unknown block for --from: $FROM_BLOCK" >&2
		exit 2
	fi

	RUN_BLOCKS=("${sliced[@]}")
fi

if [[ "$SMALL_MODE" == true ]]; then
	original_metis_odir="${METIS_ODIR-__UNSET__}"
	export METIS_ODIR="Small/"
	trap 'if [[ "$original_metis_odir" == "__UNSET__" ]]; then unset METIS_ODIR; else export METIS_ODIR="$original_metis_odir"; fi' EXIT
fi

current_block="startup"
trap 'echo "[ERROR] block=${current_block} command=${BASH_COMMAND} line=${LINENO}" >&2' ERR

total=${#RUN_BLOCKS[@]}
index=0

for block in "${RUN_BLOCKS[@]}"; do
	index=$((index + 1))
	current_block="$block"
	start_ts=$(date +%s)

	if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
		echo "::group::[$index/$total] ${block}"
	fi

	echo "[INFO] [$index/$total] Running ${block}"
	cmd=("${PYTHON_BIN}" "${BLOCK_DIR}/${block}.py")
	if [[ "$SMALL_MODE" == true ]]; then
		cmd+=("--small")
	fi
	"${cmd[@]}"

	end_ts=$(date +%s)
	elapsed=$((end_ts - start_ts))
	echo "[INFO] [$index/$total] Finished ${block} in ${elapsed}s"

	if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
		echo "::endgroup::"
	fi
done

echo "[INFO] Completed ${total} simulation blocks"
