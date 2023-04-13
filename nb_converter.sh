set +eax

DATA_DIR='data-10k/*.ipynb'
FILES="$(ls $DATA_DIR | sort -V)"
declare -a OUTPUT_DIRS=("serve/darcula" "serve/horizon" "serve/material-darker" "serve/solarized" "serve/light" "serve/dark")

for output in "${OUTPUT_DIRS[@]}";
do
	mkdir -p $output
done

for file in ${FILES[@]};
do
	jupyter nbconvert $file --to 'html' --theme "light" --output-dir="serve/light" &
	jupyter nbconvert $file --to 'html' --theme "dark" --output-dir="serve/dark" &
	jupyter nbconvert $file --to 'html' --theme "jupyterlab-horizon-theme" --output-dir="serve/horizon" &
	jupyter nbconvert $file --to 'html' --theme "jupyterlab_materialdarker" --output-dir="serve/material-darker" &
	jupyter nbconvert $file --to 'html' --theme "theme-darcula" --output-dir="serve/darcula" &
	jupyter nbconvert $file --to 'html' --theme "jupyterlab-theme-solarized-dark" --output-dir="serve/solarized" &
	wait
	echo "Completed generating $file into necessary themes"
done

