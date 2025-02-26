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

#highlight(comments)
highlight(comments, file = "C:/Users/Kathleen.Trinh/Documents/Nike/Sentiment Polarity/Highlight/Nike_Reddit_SentimentPolarityHighlight.html", open = TRUE)


do.call(rbind, reviews_02)

t(simplify2array(reviews_02))

library(stringi)
try <- stri_list2matrix(reviews_02, byrow = FALSE)


write.csv(try, file = "C:/Users/Kathleen.Trinh/Documents/Nike/Sentiment Polarity/DTM/Nike_Reddit_DTM.csv", fileEncoding="UTF-8")
write.csv(reviews_, file = "C:/Users/Kathleen.Trinh/Documents/Nike/Sentiment Polarity/Polarity Scores/Nike_Reddit_PolarityScores.csv", fileEncoding="UTF-8")