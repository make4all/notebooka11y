import pandas as pd
def readSummary(filename = 'a11y-analyze-errors-summary.csv'):
    df = pd.read_csv(filename)
    return df
def analyzeSummary(df):
    # same as df but sorted
    df.sort_values(by=['Type','Runner','count'], ascending=[True,True, False]).to_csv('sorted-11y-analyze-errors-summary.csv', index=False)
    print("file write of sorted csv to sorted-11y-analyze-errors-summary.csv")

    # group by DetailCode and filter for groups where there are lessthan 6 unique themes in each group. We are doing this to see if there are any detailcodes that don't occur in all themes.
    df.groupby('DetailCode').filter(lambda x: x['Theme'].nunique() < 6).sort_values(by=['Type','Runner','count'], ascending=[True,True, False]).to_csv('errors-less-6-a11y-analyze-errors-summary.csv', index=False)
    print("file write of df with a filter to store errors that do not occur in all themes to errors-less-6-a11y-analyze-errors-summary.csv")
    df.groupby('DetailCode').filter(lambda x: x['count'].nunique() > 1).sort_values(by=['Type','Runner','count'], ascending=[True,True, False]).to_csv('errors-different-counts-a11y-analyze-errors-summary.csv', index=False)
    print("file write of df with a filter to store errors that have different counts across themes to errors-different-counts-a11y-analyze-errors-summary.csv")

if __name__ == "__main__":
    df = readSummary()
    analyzeSummary(df)