# Tabroom Scraper

Current Status :  Can take tournament name as an input string and use that to navigate to the tournament's parli results page.
Can then navigate to prelim seeding info, sort by oppseed, save the top 32 team (by oppseed) names, their oppseed and actual seed.
Todo: Assign each team a variance and make this work with speaks as well. 

NOTE : This'll depend on final implementation, but as of right now, this will not work for tournaments that break to more than double octas. 

Program to determine accuracy of different metrics for predicting debate breaks

Currently, several large parliamentary debate tournaments, such as the National Parliamentary Debate Invitational, 
use a method known as opp seed to determine which teams will move on to elimination rounds. For those who are unfamiliar, 
oppSeed is a metric that ranks teams based on the strength of their schedule at the tournament. However, because it does 
not meet the Large Counts condition for statistical accuracy as it is only based on 3 rounds, oppSeed is often an 
inaccurate indicator for predicting good teams/breaks. 

Data from NPDI 2021 showed that speaks were a far better way to predict who went further in the tournament than oppSeed. 
This implies that speaks are the better predictor of which teams will do well, and as such, are better for evaluating 
which teams should move to elim rounds. 

The purpose of this program is to scale that calculation up easily. While calculating this data for NPDI 2021 was useful, 
it did take a while, and that was only one tournament. This program's goal is to be able to easily calculate the quality 
of both oppSeed and speaker points for every parli tournament that has published this data to get a better idea as to 
which method is better. 
