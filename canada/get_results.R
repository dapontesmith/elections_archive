setwd("C:/Users/dapon/Dropbox/Harvard/dissertation/data/constituency_level_elections_archive")

load("constituency_level_results_lower_house/clea_lc_20201216.rdata")

df <- clea_lc_20201216

canada <- df %>%
  filter(ctr_n == "Canada")
canada[canada == -990 | canada == -992] <- NA

canada <- canada %>%
  dplyr::select(-pev2, -vot2, -vv2, -ivv2, 
                -to2, -cv2, -cvs2, -pv2, -pvs2,
                -vot1, -ivv1, -to1, -release ) %>% 
  filter(yr > 1980)

setwd("C:/Users/dapon/Dropbox/Harvard/Noah_SunYoung")

write.csv(canada, "data/canada/canada_riding_1980_2019.csv")
