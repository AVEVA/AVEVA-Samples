require(testthat) 

#Path to the test folder
#For the automated build, this must be ".", if errors occur, try specifying the full path (i.e. from C:\)
path <- "."

#Suppress UI
Sys.setenv("TESTING" = TRUE)

test_results <- test_dir(path, env = test_env(), reporter="summary")

Sys.unsetenv("TESTING")


