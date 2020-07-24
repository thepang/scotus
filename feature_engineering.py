import glob

import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import variables as v

pd.set_option("display.max_columns", 40)


def get_list_of_cases():
    """
     Goes through the speech folder and grabs all the text file locations
     :return: List of all the text file locations (absolute)
     """
    all_files = list()
    files_to_parse = list()

    problem_files = [
        "/Users/pang/repos/scotus/data/006_speech/000_all.csv",
        "/Users/pang/repos/scotus/data/006_speech/138-Orig_South Carolina v. North Carolina.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-354_Sebelius v. Hobby Lobby Stores, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/105 Orig._Kansas v. Colorado.csv",
        "/Users/pang/repos/scotus/data/006_speech/18-281_Virginia House of Delegates v. Bethune-Hill.csv",
        "/Users/pang/repos/scotus/data/006_speech/130Orig_New Hampshire v. Maine.csv",
        "/Users/pang/repos/scotus/data/006_speech/141-Orig_Texas v. New Mexico.csv",
        "/Users/pang/repos/scotus/data/006_speech/18-1334_Financial Oversight and Management Bd. for Puerto Rico v. Aurelius Investment, LLC.csv",
        "/Users/pang/repos/scotus/data/006_speech/128 Orig_Alaska v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-322_Northwest Austin Municipal Util. Dist. No. One v. Holder.csv",
        "/Users/pang/repos/scotus/data/006_speech/07-77_Riley v. Kennedy.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-714_Utah v. Evans.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-333_Benisek v. Lamone.csv",
        "/Users/pang/repos/scotus/data/006_speech/14-232_Harris v. Arizona Independent Redistricting Comm'n.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-1666_Munaf  v. Geren.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-1119_Milavetz, Gallop & Milavetz, P.A. v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-205_Citizens United v. Federal Election Commission (Reargued).csv",
        "/Users/pang/repos/scotus/data/006_speech/15-1262_McCrory v. Harris.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-969_Federal Election Comm'n v. Wisconsin Right to Life, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/126-Orig_Kansas v. Nebraska.csv",
        "/Users/pang/repos/scotus/data/006_speech/18-422_Rucho v. Common Cause.csv",
        "/Users/pang/repos/scotus/data/006_speech/18-1323_June Medical Services L.L.C. v. Russo.csv",
        "/Users/pang/repos/scotus/data/006_speech/07-320_Davis v. Federal Election Comm’n.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-240_Mac's Shell Service, Inc. v.  Shell Oil Products Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/05-204_League of United Latin American Citizens v. Perry.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1472_Cherokee Nation of Okla. v. Thompson.csv",
        "/Users/pang/repos/scotus/data/006_speech/132-Orig._Alabama v. North Carolina.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-134_New Jersey v. Delaware.csv",
        "/Users/pang/repos/scotus/data/006_speech/18-726_Lamone v. Benisek.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-1314_Arizona State Legislature v. Arizona Independent Redistricting Comm'n.csv",
        "/Users/pang/repos/scotus/data/006_speech/12-536_McCutcheon v. Federal Election Comm'n.csv",
        "/Users/pang/repos/scotus/data/006_speech/14-940_Evenwel v. Abbott.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1437_Branch v. Smith.csv",
        "/Users/pang/repos/scotus/data/006_speech/129 Orig._Virginia v. Marylan.csv",
        "/Users/pang/repos/scotus/data/006_speech/142-Orig_Florida v. Georgia.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-586_Abbott v. Perez.csv",
        "/Users/pang/repos/scotus/data/006_speech/137-Orig_Montana v. Wyoming.csv",
        "/Users/pang/repos/scotus/data/006_speech/16-1161_Gill v. Whitfor.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1674_McConnell v. Federal Election Comm'n.csv",
        "/Users/pang/repos/scotus/data/006_speech/105orig_Kansas v. Colorado.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-680_Bethune-Hill v. Virginia State Bd. of Elections.csv",
        "/Users/pang/repos/scotus/data/006_speech/14-1504_Wittman v. Personhuballah.csv",
        "/Users/pang/repos/scotus/data/006_speech/09-1233_Schwarzenegger v. Plata.csv",
        "/Users/pang/repos/scotus/data/006_speech/11-713_Perry v. Perez.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-1498_Holder v. Humanitarian Law Project.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1864_Hunt v. Cromartie.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-618_Office of Sen. Mark Dayton v. Hanson.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-596_Lorillard Tobacco Co. v. Reilly.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1132_Illinois v. McArthur.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-271_Dow Chemical Co. v. Stephenson.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-1237_Merck KGaA v. Integra Lifesciences I, LTD.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-10873_Khanh Phuong Nguyen v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-9136_Daniels v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/11-184_Kloeckner v. Solis.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-344_Thompson v. Western States Medical Center.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-549_Cedric Kushner Promotions, Ltd. v. King.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-800_Howsam v. Dean Witter Reynolds, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/05-1382_Gonzales v. Planned Parenthood Federation of America, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-984_Jose Ernesto Medellin, v. Texas.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-653_FCC v. NextWave Personal Communications Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-973_United States v. Vonn.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-391_Florida v. Thomas.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1377_Doe v. Chao.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-763_Barnhart v. Thomas.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-46_Federal Maritime Comm'n. v. South Carolina Ports Authority.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-705_Barnhart v. Peabody Coal Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-704_United States v. Bean.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1184_United States v. Jimenez Recio.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-5554_Hiibel v. Sixth Judicial Dist. Court of Nev., Humboldt Cty.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-799_Los Angeles v. Alameda Books, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-679_Gonzaga Univ. v. Doe.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-371_Virginia v. Hicks.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-358_Department of Transportation v. Public Citizen.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-189_Idaho v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-473_United States v. Banks.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-511_Verizon Communications, Inc. v. FCC.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-408_Holmes Group, Inc. v. Vornado Air Circulation Systems, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-516_Gratz v. Bollinger.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-957_Kansas v. Crane.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-306_Beneficial Nat. Bank v. Anderson.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-453_Cuomo v. Clearing House Assn., L.L.C.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-618_Eldred v. Ashcroft.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1016_Till v. SCS Credit Cor.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1368_Nevada Dept. of Human Resources v. Hibbs.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1657_Scarborough v. Principi.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-804_Cleveland v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1806_Madigan v. Telemarketing Associates, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-694_United States v. Williams.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-832_National Cable & Telecommunications Assn., Inc. v. Gulf Power Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-584_Adams v. Florida Power Cor.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-963_Norfolk & Western R. Co. v. Ayers.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-6418_Welch v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-7662_Miller-El v. Cockrell.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-258_Jinks v. Richland County.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1964_Booth v. Churner.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-417_Devlin v. Scardelletti.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1491_Demore v. Hyung Joon Kim.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-518_BE&K Constr. Co. v. NLRB.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1389_United States v. Galletti.csv",
        "/Users/pang/repos/scotus/data/006_speech/09-10876_Bullcoming v. New Mexico.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1603_Beard v. Banks.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-188_Pharmaceutical Research and Mfrs. of America v. Concannon.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1908_Alexander v. Sandoval.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1183_United States v. Patane.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-6677_Penry v. Johnson.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-9073_Buford v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-693_Lamie v. United States Trustee.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1519_United States v. Arvizu.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-706_Sprietsma v. Mercury Marine.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1038_Eastern Associated Coal Corp. v. Mine Workers.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1406_Chevron U. S. A., Inc. v. Echazabal.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-507_Chickasaw Nation v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-631_United States v. Drayton.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-151_United States v. Oakland Cannabis Buyers' Cooperative.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-309_Hope v. Pelzer.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-301_Carey v. Saffol.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1687_Bartnicki v. Vopper.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-521_Republican Party of Minn. v. White.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-361_United States v. American Library Assn., Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-5165_Thornton v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/12-96_Shelby County v. Holder.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-428_Dastar Corp. v. Twentieth  Century Fox Film Cor.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1792_Director of Revenue of Mo. v. CoBank ACB.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-270_Yellow Transp. Inc. v. Michigan, et al.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-795_Ashcroft v. Free Speech Coalition.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-568_New York v. FERC.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-722_American Ins. Assn. v. Garamendi.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-628_Frew v. Hawkins.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-461_American Broadcasting Co.  v. Aereo, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-1039_Sandoz Inc. v. Amgen Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-215_Pacificare Health Systems, Inc. v. Book.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1613_Shaw v. Murphy.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-936_Ferguson v. Charleston.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1080_General Dynamics Land Systems, Inc. v. Cline.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1293_Ashcroft v. American Civil Liberties Union.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-218_Ashcroft v. American Civil Liberties Union.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-10038_Tennard v. Dretke.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1809_Hibbs v. Winn.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-394_Christopher v. Harbury.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1238_Nixon v. Missouri Municipal League.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1609_City of Littleton v. Z.J. Gifts D-4, L.L.C.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-666_Department of Revenue of Ky. v. Davis.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1435_Clackamas Gastroenterology Associates, P. C. v. Wells.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-147_SEC v. Zandfor.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1444_Chavez v. Martinez.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1167_Tahoe-Sierra Pres. Council, Inc. v. Tahoe Reg. Planning Agency.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-281_Inyo County v. Paiute-Shoshone Indians of Bishop Community of Bishop Colony.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-130_Lucia v. SEC.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-682_Barnes v. Gorman.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-241_Grutter v. Bollinger.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-9065_Muhammad v. Close.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-575_Nike, Inc. v. Kasky.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-767_INS v. St. Cyr.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1089_Toyota Motor Mfg., Ky., Inc. v. Williams.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1214_Alabama v. Shelton.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-954_Office of Independent Counsel v. Favish.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1426_American Trucking Assns., Inc. v. Browner.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1884_Lackawanna County District Attorney v. Coss.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1238_Artuz v. Bennett.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-809_Maryland v. Pringle.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1606_Tennessee Student Assistance Corporation v. Hoo.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-10666_Harris v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1257_Browner v. American Trucking Assns., Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-203_United States v. Cleveland Indians Baseball Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1348_Olympic Airways v. Husain.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-376_Hinck v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-407_Kowalski v. Tesmer.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-811_Groh v. Ramirez.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-2035_Cooper Industries, Inc. v. Leatherman Tool Group, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-6539_Johnson v. California.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-107_United States v. Lara.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-6029_Ragsdale v. Wolverine World Wide, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-167_United States v. Dominguez Benitez.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-8576_Glover v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1770_Department of Housing and Urban Development v. Rucker.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1030_Indianapolis v. Edmon.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-69_Roell v. Withrow.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1953_District of Columbia v. Tri County Industries, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1937_Barnhart v. Walton.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-6978_Ewing v. California.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1543_Festo Corp. v. Shoketsu Kinzoku Kogyo Kabushiki Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1571_TrafFix Devices, Inc. v. Marketing Displays, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1379_Circuit City Stores v. Adams.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1567_Young v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-593_Dole Food Co. v. Patrickson.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1375_United States v. Navajo Nation.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1127_Lockyer v. Andrade.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-103_Reed Elsevier, Inc. v. Muchnick.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-537_Bravo-Fernandez v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/07-308_United States v. Clintwood Elkhorn Mining Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-346_Norfolk Shipbuilding & Drydock Corp. v. Garris.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-9094_Abdur'Rahman v. Bell.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1295_Gitlitz v. Commissioner.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-475_Cheney v. United States Dist. Court for D. C.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-5991_Shaw v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-146_Arthur Andersen LLP  v. Carlisle.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-5250_Shafer v. South Carolina.csv",
        "/Users/pang/repos/scotus/data/006_speech/12-930_Mayorkas v. Cuellar de Osorio.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-9280_Kelly v. South Carolina.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1551_Semtek International Inc. v. Lockheed Martin Cor.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-102_Lawrence v. Texas.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-860_Correctional Services Corp. v. Malesko.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-455_Franconia Associates v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1994_Nevada v. Hicks.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1757_Stogner v. California.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1343_Engine Mfrs. Assn. v. South Coast Air Quality Management Dist.csv",
        "/Users/pang/repos/scotus/data/006_speech/05-746_Norfolk Southern R. Co. v. Sorrell.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1205_Jones v. R. R. Donnelley & Sons Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1853_Swierkiewicz v. Sorema N. A.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1021_Rush Prudential HMO, Inc. v. Moran.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-337_Breuer v. Jim's Concrete of Brevar.csv"
        "/Users/pang/repos/scotus/data/006_speech/01-1289_State Farm Mut. Automobile Ins. Co. v. Campbell.csv",
        "/Users/pang/repos/scotus/data/006_speech/11-9307_Henderson v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1187_McKune v. Lile.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-6821_Nelson v. Campbell.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-1164_Veneman v. Livestock Marketing Assn.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-911_Kucana v. Holder.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1977_Saucier v. Katz.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-1618_Bostock v. Clayton County.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-9285_Mickens v. Taylor.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-724_F. Hoffmann-LaRoche, Ltd. v. Empagran S.A.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-651_JP Morgan Chase Bank v. Traffic Stream (BVI) Infrastructure Lt.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-5961_Tyler v. Cain.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-878_Mathias v. Worldcom Technologies, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-221_Pliler v. For.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1541_Iowa v. Tovar.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1786_Great-West Life & Annuity Ins. Co. v. Knudson.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-403_Federal Election Comm'n v. Beaumont.csv",
        "/Users/pang/repos/scotus/data/006_speech/07-8521_Harbison v. Bell.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1593_BedRoc Limited, LLC v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1831_United States v. Craft.csv",
        "/Users/pang/repos/scotus/data/006_speech/12-417_Sandifer v. United States Steel Cor.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-42_Franchise Tax Bd. of Cal. v. Hyatt.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1420_Washington State Dept. of Social and Health Servs. v. Guardianship Estate of Keffeler.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-586_Jones v. Harris Associates L.P.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-950_Hillside Dairy Inc. v. Lyons.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-400_Bell v. Cone.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-757_Syngenta Crop Protection, Inc. v. Henson.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-777_Samsung Electronics Co., v. Apple Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-332_Board of Ed. Dist. No. 92 of Pottawatomie Cty. v. Earls.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1689_Grupo Dataflux v. Atlas Global Grou.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-192_Abuelhawa v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1260_United States v. Knights.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-95_Pennsylvania State Police v. Suders.csv",
        "/Users/pang/repos/scotus/data/006_speech/98-1768_Buckman Company v. Plaintiffs' Legal Committee.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-43_Dahda v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-927_Chao v. Mallard Bay Drilling, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-929_Cook v. Gralike.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-853_Porter v. Nussle.csv",
        "/Users/pang/repos/scotus/data/006_speech/04-623_Gonzales v. Oregon.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1751_Zelman v. Simmons-Harris.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1794_United States v. Flores-Montano.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1185_Seling v. Young.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1178_Solid Waste Agency of No. Cook Cty. v. Army Corps of Engineers.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1243_Borden Ranch Partnership v. Army Corps of Engineers.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-9130_Ali v. Federal Bureau of Prisons.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-2047_Palazzolo v. Rhode Islan.csv",
        "/Users/pang/repos/scotus/data/006_speech/06-1265_Klein & Co. Futures v. Board of Trade of City of New York.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1209_The Boeing Co. v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1871_Department of Interior v. Klamath Water Users Protective Assn.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1307_Massanari v. Sigmon Coal Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1500_Clay v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1011_Calcano-Martinez v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-191_Federal Election Comm'n v. Colorado Republican Fed. Campaign Comm.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-8452_Atkins v. Virginia.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-682_Verizon Comm. Inc. v. Law Offices of Curtis V. Trinko LLP.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1702_Texas v. Cobb.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-763_Pollard v. E. I. duPont de Nemours & Co.csv",
        "/Users/pang/repos/scotus/data/006_speech/16-349_Henson v. Santander Consumer USA Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1572_Cook County v. United States, ex rel. Chandler.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1531_Verizon Md. Inc. v. Public Serv. Comm'n of M.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-634_Green Tree Financial Corp. v. Bazzle.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1045_TRW Inc. v. Andrews.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1737_Watchtower Bible & Tract Soc. of N. Y. v. Village of Stratton.csv",
        "/Users/pang/repos/scotus/data/006_speech/04-721_Evans v. Chavis.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-526_Schriro v. Summerlin.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-454_Atkinson Trading Co. v. Shirley.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1067_United States v. White Mountain Apache Tribe.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-901_Brentwood Academy v. Tennessee Secondary Athletic Assn.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1514_Raygor v. Regents of Univ. of Minn.csv",
        "/Users/pang/repos/scotus/data/006_speech/08-441_Gross v. FBL Financial Services, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1196_SEC v. Edwards.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1824_Dretke v. Haley.csv",
        "/Users/pang/repos/scotus/data/006_speech/09-6822_Pepper v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-6683_Castro v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-1238_IBP, Inc. v. Alvarez.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-101_Norton v. Southern Utah Wilderness Alliance.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-9410_Crawford v. Washington.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-730._Adarand Constructors, Inc. v. Mineta.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-729_Smith v. Doe.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-182_Georgia v. Ashcroft.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-334_Rasul v. Bush.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-121_Duncan v. Walker.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-276_United States v. United Foods, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-292_C & L Enterprises, Inc. v. Citizen Band Potawatomi Tribe of Okla.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1107_Virginia v. Black.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-201_New York Times Co. v. Tasini.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-603_Legal Services Corporation v. Velazquez.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-6320_Fellers v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-298_Lapides v. Board of Regents of Univ. System of Ga.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1269_Cuyahoga Falls v. Buckeye Community Hope Foundation.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-1433_Brumfield v. Cain.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1229_Pierce County v. Guillen.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-1606_Smith v. Berryhill.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-819_Kontrick v. Ryan.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-952_Wisconsin Dept. of Health and Family Servs. v. Blumer.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-695_Fitzgerald v. Racing Assn. of Central Iowa.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-8508_Kyllo v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-626_South Fla. Water Management Dist. v. Miccosukee Tribe.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1624_Elk Grove Unified School Dist. v. Newdow.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-7504_Lopez v. Davis.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1471_Kentucky Assn. of Health Plans, Inc. v. Miller.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1240_Board of Trustees of the Univ. of Ala. v. Garrett.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-6696_Hamdi v. Rumsfel.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-758_Postal Service v. Gregory.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-469_Black & Decker Disability Plan v. Nor.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-131_Gisbrecht v. Barnhart.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-687_United States v. Cotton.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1614_National Railroad Passenger Corporation v. Morgan.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-157_United Dominion Industries, Inc. v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-6933_Lee v. Kemna.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1848_Buckhannon Board & Care Home, Inc. v. West Virginia Dept. of Health and Human Resources.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1315_Locke v. Davey.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1580_Vieth v. Jubelirer.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-8286_Banks v. Dretke.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-492_Alabama v. Bozeman.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1060_Illinois v. Lidster.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-458_Raymon.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-419_Columbus v. Ours Garage & Wrecker Service, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1680_City News & Novelty, Inc. v. Waukesha.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-2036_Good News Club v. Milford Central School.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-463_United States v. Fior D'Italia, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-196_National Park Hospitality Assn. v. Department of Interior.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-628_Salman v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-949_Bush v. Gore.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1290_Postal Service v. Flamingo Industries (USA) Lt.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-595_United States v. Ruiz.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1235_Green Tree Financial Corp.-Ala. v. Randolph.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1231_Connecticut Dept. of Public Safety v. Doe.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-233_Puerto Rico v. Franklin Cal. Tax-Free Trust.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-13_Republic of Austria v. Altmann.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-7574_Sattazahn v. Pennsylvania.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-964_Baldwin v. Reese.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1118_Scheidler v. National Organization for Women, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1434_United States v. Mead Cor.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-572_Intel Corp. v. Advanced Micro Devices, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1978_United States v. Hatter.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-749_Raytheon Co. v. Hernandez.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-24_PGA Tour, Inc. v. Martin.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-1175_Los Angeles v. Patel.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-896_Ford Motor Co. v. McCauley.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-2071_Tuan Anh v. INS.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1015_Moseley v. V. Secret Catalogue, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-347_Wharf (Holdings) Ltd. v. United Int'l Holdings, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1331_Lewis v. Lewis & Clark Marine, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/09-1227_Bond v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1249_Thomas v. Chicago Park Dist.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1073_Owasso Independent School Dist. No. I-011 v. Falvo.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-5664_Sell v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-819_Kontrick v. Ryan.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-152_Lujan v. G & G Fire Sprinklers, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1632_Blakely v. Washington.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-6218_Rogers v. Tennessee.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-6567_Dusenbery v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-859_Central Green Co. v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-339_Francisco Soso v. Alvarez-Machain.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-299_Entergy La., Inc. v. Louisiana Pub. Serv. Comm'n.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1559_Massaro v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1815_NLRB v. Kentucky River Community Care, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1408_Atwater v. Largo Vista.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1250_US Airways, Inc. v. Barnett.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1684_Yarborough v. Alvarado.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-524_Price v. Vincent.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1325_Washington Legal Foundation v. Legal Foundation of Wash.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-658_Alaska Dept. of Environmental Conservation v. EPA.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-1027_Rumsfeld v. Padilla.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1862_Woodford v. Garceau.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1120_Meyer v. Holly.csv",
        "/Users/pang/repos/scotus/data/006_speech/11-5683_Dorsey v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-836_Bush v. Palm Beach County Canvassing Boar.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-311_Wiggins v. Smith.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-895_Alabama Legislative Black Caucus v. Alabama.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1823_EEOC v. Waffle House, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1371_Missouri v. Siebert.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1529_Egelhoff v. Egelho.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-6374_Becker v. Montgomery.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-7791_Zadvydas v. Underdown.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1595_Hoffman Plastic Compounds, Inc. v. NLRB.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-1667_Tennessee v. Lane.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1418_Archer v. Warner.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-488_Ring v. Arizona.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-857_Household Credit Services, Inc. v. Pfennig.csv",
        "/Users/pang/repos/scotus/data/006_speech/00-1072_Edelman v. Lynchburg College.csv",
        "/Users/pang/repos/scotus/data/006_speech/03-44_Sabri v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/99-1996_J. E. M. Ag Supply, Inc. v. Pioneer Hi-Bred International, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-679_Desert Palace, Inc. v. Costa.csv",
        "/Users/pang/repos/scotus/data/006_speech/10-7387_Setser v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-337_Breuer v. Jim's Concrete of Brevar.csv",
        "/Users/pang/repos/scotus/data/006_speech/01-1289_State Farm Mut. Automobile Ins. Co. v. Campbell.csv",
        "/Users/pang/repos/scotus/data/006_speech/02-891_Central Laborers' Pension Fund v. Heinz.csv",
    ]

    for text_path in glob.glob(f"{v.ROOT_PATH}/{v.SPEECH_FOLDER}/*"):
        all_files.append(text_path)

    for file in all_files:
        if file not in problem_files:
            files_to_parse.append(file)
        else:
            print(f"Skipping: {file}")

    return files_to_parse


def num_speak_data():
    def count_num(text):
        """
          Counts the number of times a speaker speaks in a given transcript
          :param text: text to find speaker counts
          :return: petitioner_judge, petitioner_lawyer, respondent_judge, respondent_lawyer
          """
        speaker_cts = text.groupby(by=["party", "speaker_type"]).count().reset_index()

        return speaker_cts["speaker"].tolist()

    files = get_list_of_cases()
    to_df = []
    for file in files:
        try:
            (
                petitioner_judge,
                petitioner_lawyer,
                respondent_judge,
                respondent_lawyer,
            ) = count_num(pd.read_csv(file))
            to_df.append(
                [
                    file.split("/")[-1].split("_")[0],
                    petitioner_judge,
                    petitioner_lawyer,
                    respondent_judge,
                    respondent_lawyer,
                ]
            )
        except ValueError:
            print(f"'{file}',")
    df = pd.DataFrame(
        to_df,
        columns=[
            "docket",
            "speak_num_pet_jdg",
            "speak_num_pet_law",
            "speak_num_res_jdg",
            "speak_num_res_law",
        ],
    )
    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/num_speak_data.csv", index=False)
    return None


def num_interruptions():
    def count_interruptions(text):
        """
          Counts the number of times a speaker is interrupted by looking for sentences that end in "--"
          :return: pj_interrupt, pl_interrupt, rj_interrupt, rl_interrupt
          """

        text["interrupt_count"] = np.where(
            text["text"].str.contains(r"--$", regex=True), 1, 0
        )
        df = text.groupby(by=["party", "speaker_type"]).sum().reset_index()

        pj, pl, rj, rl = df["interrupt_count"].tolist()
        return pj, pl, rj, rl, text

    full_df = pd.DataFrame(
        columns=["party", "speaker_type", "speaker", "text", "interrupt_count"]
    )
    files = get_list_of_cases()
    to_df = []

    # columns = [party,speaker_type,speaker,text,interrupt_count]
    # df = pd.DataFrame(columns=columns)

    for file in files:
        try:
            (
                pj_interrupt,
                pl_interrupt,
                rj_interrupt,
                rl_interrupt,
                docket_df,
            ) = count_interruptions(pd.read_csv(file))
            docket_df["docket"] = file.split("/")[-1].split("_")[0]
            full_df = full_df.append(docket_df, ignore_index=False)
            to_df.append(
                [
                    file.split("/")[-1].split("_")[0],
                    pj_interrupt,
                    pl_interrupt,
                    rj_interrupt,
                    rl_interrupt,
                ]
            )
        except ValueError:
            print(f'"{file}",')

    df = pd.DataFrame(
        to_df,
        columns=[
            "docket",
            "pj_interrupted",
            "pl_interrupted",
            "rj_interrupted",
            "rl_interrupted",
        ],
    )

    full_df.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_interruption_count.csv",
        columns=[
            "docket",
            "party",
            "speaker_type",
            "speaker",
            "text",
            "interrupt_count",
        ],
        index=False,
    )
    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/interruption_data.csv", index=False)
    return None


def sentiment_scores():
    def get_sentiment(df):
        analyzer = SentimentIntensityAnalyzer()

        columns = ["neg", "pos", "neu", "compound"]

        for name in columns:
            df[name] = 0

        for index, row in df.iterrows():
            try:
                vs = analyzer.polarity_scores(row["text"])
                for score in columns:
                    df.loc[index, score] = vs[score]
            except AttributeError:
                pass

        sum_df = df.groupby(by=["party", "speaker_type"]).mean().reset_index()
        sentiments = list()

        for name in columns:
            for item in sum_df[name].values:
                sentiments.append(item)

        return sentiments, df

    files = get_list_of_cases()
    to_df = []
    full_data = pd.DataFrame()

    for file in files:
        print(f"Processing: {file})")
        docket_num = file.split("/")[-1].split("_")[0]

        scores, df = get_sentiment(pd.read_csv(file))
        df["docket"] = docket_num
        full_data = full_data.append(df, ignore_index=False)
        temp_ = [docket_num]

        [temp_.append(item) for item in scores]
        to_df.append(temp_)

    df = pd.DataFrame(
        to_df,
        columns=[
            "docket",
            "pj_sent_neg",
            "pl_sent_neg",
            "rj_sent_neg",
            "rl_sent_neg",
            "pj_sent_pos",
            "pl_sent_pos",
            "rj_sent_pos",
            "rl_sent_pos",
            "pj_sent_neu",
            "pl_sent_neu",
            "rj_sent_neu",
            "rl_sent_neu",
            "pj_sent_compound",
            "pl_sent_compound",
            "rj_sent_compound",
            "rl_sent_compound",
        ],
    )

    full_data.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_sentiment_data.csv",
        columns=[
            "docket",
            "party",
            "speaker_type",
            "speaker",
            "text",
            "neg",
            "pos",
            "neu",
            "compound",
        ],
        index=False,
    )
    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/sentiment_data.csv", index=False)
    return None


def num_word_counts():
    def count_words(text):
        """
          Counts the number of times a speaker is interrupted by looking for sentences that end in "--"
          :return: pj_interrupt, pl_interrupt, rj_interrupt, rl_interrupt
          """

        text["word_count"] = 0
        for index, row in text.iterrows():
            words = str(row["text"]).split(" ")
            text.loc[index, "word_count"] = len(words)

        df = text.groupby(by=["party", "speaker_type"]).sum().reset_index()

        pj, pl, rj, rl = df["word_count"].tolist()

        return pj, pl, rj, rl, text

    files = get_list_of_cases()
    to_df = []
    full_df = pd.DataFrame()

    for file in files:
        print(f"Processing: {file})")

        docket_num = file.split("/")[-1].split("_")[0]
        (
            pj_word_count,
            pl_word_count,
            rj_word_count,
            rl_word_count,
            text_df,
        ) = count_words(pd.read_csv(file))

        text_df["docket"] = docket_num
        to_df.append(
            [docket_num, pj_word_count, pl_word_count, rj_word_count, rl_word_count]
        )
        full_df = full_df.append(text_df, ignore_index=False)
    df = pd.DataFrame(
        to_df,
        columns=[
            "docket",
            "pj_word_count",
            "pl_word_count",
            "rj_word_count",
            "rl_word_count",
        ],
    )
    full_df.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_word_count_data.csv",
        columns=["docket", "party", "speaker_type", "speaker", "text", "word_count"],
        index=False,
    )
    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/num_word_count_data.csv", index=False)
    return None


def num_short_exchanges():
    test = pd.read_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_word_count_data.csv")
    test = (
        test[test["word_count"] < 5]
        .groupby(by=["docket", "party", "speaker_type"])
        .count()
        .reset_index()
    )
    dockets = test["docket"].unique()

    dictionary = dict()

    for docket in dockets:
        docket_subset = test[test["docket"] == docket].sort_values(
            by=["docket", "party", "speaker_type"]
        )
        counts = dict()

        for index, row in docket_subset.iterrows():
            if row["party"] == "petitioner" and row["speaker_type"] == "lawyer":
                variable = "short_x_pl"
            elif row["party"] == "petitioner" and row["speaker_type"] == "judge":
                variable = "short_x_pj"
            elif row["party"] == "respondent" and row["speaker_type"] == "lawyer":
                variable = "short_x_rl"
            elif row["party"] == "respondent" and row["speaker_type"] == "judge":
                variable = "short_x_rj"
            counts[variable] = row["word_count"]

        dictionary[docket] = counts

    full_data = pd.DataFrame(dictionary).T
    full_data = full_data.fillna(0)

    full_data.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/short_exchange_count.csv",
        index_label="docket",
    )

    return None


def num_stutter():
    all_words = pd.read_csv("/Users/pang/repos/scotus/data/007_features/words.csv")
    full_stutter_counts = dict()
    for index, row in all_words.iterrows():
        row_count = dict()
        for item in row.index.values:
            if item == "docket":
                docket = row[item]
            elif item == "pj_text":
                row_count["pj_stutter_ct"] = str(row[item]).count(" -- ")
            elif item == "pl_text":
                row_count["pl_stutter_ct"] = str(row[item]).count(" -- ")
            elif item == "rj_text":
                row_count["rj_stutter_ct"] = str(row[item]).count(" -- ")
            elif item == "rl_text":
                row_count["rl_stutter_ct"] = str(row[item]).count(" -- ")
            else:
                print("Shouldn't hit this")
        full_stutter_counts[docket] = row_count
    df = pd.DataFrame(full_stutter_counts).T

    df.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_stutter_count.csv",
        index_label="docket",
    )

    return None


# num_speak_data()
# num_interruptions()
# sentiment_scores()
# num_word_counts()
# num_short_exchanges()
num_stutter()
