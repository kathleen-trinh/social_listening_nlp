library(ggplot2)
library(ggExtra)
library(magrittr)
library(dplyr)
library(sentimentr)
library(data.table)
library(lubridate)
library(rlang)
library(gofastr)
library(termco)

dat <- data.frame(read.csv(file.choose()))
dat <- setDT(dat)
get_sentences(dat)
reviews <- get_sentences(dat)
reviews_ <- sentiment(reviews)
reviews_01 <- sentiment_attributes(reviews)
reviews_02 <- extract_sentiment_terms(reviews)
comments <- sentiment_by(reviews)

# Need to include this line before using highlight function due to error:
# Error in `[.data.table`(y, , list(sentiment = attributes(x)[["averaging.function"]](sentiment),  : 
# attempt to apply non-function
attr(comments, "averaging.function") <- sentimentr::average_downweighted_zero

#highlight( comments)
highlight(comments, file = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/YouTube/Nissan_LEAF_YouTube_SentimentPolarityHighlight.html", open = TRUE)


do.call(rbind, reviews_02)

t(simplify2array(reviews_02))

library(stringi)
try <- stri_list2matrix(reviews_02, byrow = FALSE)


write.csv(try, file = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/YouTube/Nissan_LEAF_YouTube_DTM.csv", fileEncoding="UTF-8")
write.csv(reviews_, file = "C://Users/kathleen.trinh/Documents/Nissan/LEAF/YouTube/Nissan_LEAF_YouTube_PolarityScores.csv", fileEncoding="UTF-8")