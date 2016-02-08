ifolder <- "/media/user/data/AWC-IN_022016"

data_folder <- file.path(ifolder, 'downloads')

files_string <- list.files(path= data_folder, pattern = glob2rx('*.zip'))
length(files_string)

print (files_string)

for (characters in files_string){
	unzip(file.path(data_folder, characters), exdir = file.path(ifolder, 'unzipped_d'))
	}

unzip('/media/user/data/files_1454926840.zip')	
 	