package gui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.ComboBoxModel;
import javax.swing.DefaultComboBoxModel;
import javax.swing.GroupLayout;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.LayoutStyle;



/**
* This code was edited or generated using CloudGarden's Jigloo
* SWT/Swing GUI Builder, which is free for non-commercial
* use. If Jigloo is being used commercially (ie, by a corporation,
* company or business for any purpose whatever) then you
* should purchase a license for each developer using Jigloo.
* Please visit www.cloudgarden.com for details.
* Use of Jigloo implies acceptance of these licensing terms.
* A COMMERCIAL LICENSE HAS NOT BEEN PURCHASED FOR
* THIS MACHINE, SO JIGLOO OR THIS CODE CANNOT BE USED
* LEGALLY FOR ANY CORPORATE OR COMMERCIAL PURPOSE.
*/
public class KeeperGUI extends BorrowerGUI{
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	private JButton lendBook;
	private JLabel listOfBooksRequestedFromCentralLibraryLabel;
	private JPanel searchForBookPanelInsideJPane;
	private JTabbedPane tabbedPaneForTheSearch;
	private JPanel lendBookPanel;
	private JButton listOfBooksRequestedFromCentralLibraryMarkAsReceivedButton;
	private JScrollPane listOfBooksRequestedFromCentralLibraryScrollBar;
	private JPanel listOfBooksRequestedFromCentralLibraryPanel;
	protected JButton removeKeeperButton;
	protected JButton addKeeperButton;
	private JButton requestReturnOfABookInTheList;
	private JScrollPane userSearchResultScrollPane;
	private JComboBox userSearchCriteriaChoiceList;
	private JScrollPane jScrollPane1;
	private JTextField whateverYourCriteriaIsFiel;
	private JButton searchInitiatorButton;
	private JPanel searchForUSerPanel;
	private JButton jButton1;
	private JButton startSearchbutton;
	private JButton approveLoanButtonInsideLendBookSubPanelofCentrePanel;
	private JTextField jTextField1;
	private JComboBox jComboBox1;
	private JPanel jPanel1;
	private JScrollPane bookResultScrollPane;
	private JTextField searchBoxForBook;
	private JComboBox bookCriteria;
	private JPanel searchForUserPanelInsideJPane;

	/*
	private JLabel listOfBooksCurrentlyRequestedForLabel;
	private JButton markAsReceivedButton;
	private JScrollPane listOfBooksRequestedFromCentralLibrary;*/

	private JButton searchForUser;
	private JButton viewRequestRecord ;
	
	public KeeperGUI(String name){
		super(name);
		initGUI(name);

		this.setVisible(true);
		
		//start
		
		//remebr what you did to add and remove keeper
		{
			addKeeperButton = new JButton();
			addKeeperButton.setText("Add as Keeper");
			addKeeperButton.setVisible(false);
		}
		{
			removeKeeperButton = new JButton();
			removeKeeperButton.setText("Remove Keeper");
			removeKeeperButton.setVisible(false);
		}
		
		//end
		
	}
	
	//TODO this would have to go after this development stage
	public KeeperGUI(){
		super();
		//TODO get rid of this comon
		initGUI("comon");
		//start
		
		//end
		this.setVisible(true);
	}
	
	private void initGUI(String s){
		
		lendBook = new JButton("Lend Book");
		lendBook.addActionListener(new LendBookListener());
		
		searchForUser = new JButton("User Search");
		searchForUser.addActionListener(new UserSearchListener());
		
		viewRequestRecord = new JButton("Request Record");
		viewRequestRecord.addActionListener(new ViewRequestRecordListener());

		west.add(viewRequestRecord);
		viewRequestRecord.setToolTipText("displays the list of books currently requested by the branc");
		west.add(lendBook);
		lendBook.setToolTipText("click this button if you would like to lend a book out");
		west.add(searchForUser);
		searchForUser.setToolTipText("use this to search for a user \r\nand make a book return request");
		
		west.add(new JLabel("            "));
		
		submitRequestButton.setVisible(true);
		markAsSentButton.setVisible(true);
		recordBookReturn.setVisible(true);
		
	}
	
	private class ViewRequestRecordListener implements ActionListener{
		
		public void actionPerformed(ActionEvent e){
			System.out.println("View Request Record Button Clicked");
			KeeperGUI.this.centre.removeAll();
			
			{
				listOfBooksRequestedFromCentralLibraryPanel = new JPanel();
				GroupLayout listOfBooksRequestedFromCentralLibraryPanelLayout = new GroupLayout((JComponent)listOfBooksRequestedFromCentralLibraryPanel);
				listOfBooksRequestedFromCentralLibraryPanel.setLayout(listOfBooksRequestedFromCentralLibraryPanelLayout);
				KeeperGUI.this.centre.add(listOfBooksRequestedFromCentralLibraryPanel);
				listOfBooksRequestedFromCentralLibraryPanel.setPreferredSize(new java.awt.Dimension(480, 465));
				{
					listOfBooksRequestedFromCentralLibraryScrollBar = new JScrollPane();
				}
				{
					listOfBooksRequestedFromCentralLibraryMarkAsReceivedButton = new JButton();
					listOfBooksRequestedFromCentralLibraryMarkAsReceivedButton.setText("Mark as Received");
				}
				{
					listOfBooksRequestedFromCentralLibraryLabel = new JLabel();
					listOfBooksRequestedFromCentralLibraryLabel.setText("List of Books currently requested from Main Library");
				}
					listOfBooksRequestedFromCentralLibraryPanelLayout.setHorizontalGroup(listOfBooksRequestedFromCentralLibraryPanelLayout.createSequentialGroup()
					.addContainerGap(61, 61)
					.addGroup(listOfBooksRequestedFromCentralLibraryPanelLayout.createParallelGroup()
					    .addGroup(listOfBooksRequestedFromCentralLibraryPanelLayout.createSequentialGroup()
					        .addComponent(listOfBooksRequestedFromCentralLibraryScrollBar, GroupLayout.PREFERRED_SIZE, 350, GroupLayout.PREFERRED_SIZE)
					        .addGap(0, 0, Short.MAX_VALUE))
					    .addGroup(listOfBooksRequestedFromCentralLibraryPanelLayout.createSequentialGroup()
					        .addGap(38)
					        .addGroup(listOfBooksRequestedFromCentralLibraryPanelLayout.createParallelGroup()
					            .addGroup(listOfBooksRequestedFromCentralLibraryPanelLayout.createSequentialGroup()
					                .addComponent(listOfBooksRequestedFromCentralLibraryLabel, GroupLayout.PREFERRED_SIZE, 303, GroupLayout.PREFERRED_SIZE)
					                .addGap(0, 0, Short.MAX_VALUE))
					            .addGroup(GroupLayout.Alignment.LEADING, listOfBooksRequestedFromCentralLibraryPanelLayout.createSequentialGroup()
					                .addGap(61)
					                .addComponent(listOfBooksRequestedFromCentralLibraryMarkAsReceivedButton, GroupLayout.PREFERRED_SIZE, 161, GroupLayout.PREFERRED_SIZE)
					                .addGap(0, 81, Short.MAX_VALUE)))
					        .addGap(9)))
					.addContainerGap(69, 69));
					listOfBooksRequestedFromCentralLibraryPanelLayout.setVerticalGroup(listOfBooksRequestedFromCentralLibraryPanelLayout.createSequentialGroup()
					.addContainerGap(23, 23)
					.addComponent(listOfBooksRequestedFromCentralLibraryLabel, GroupLayout.PREFERRED_SIZE, 20, GroupLayout.PREFERRED_SIZE)
					.addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED, 1, Short.MAX_VALUE)
					.addComponent(listOfBooksRequestedFromCentralLibraryScrollBar, GroupLayout.PREFERRED_SIZE, 354, GroupLayout.PREFERRED_SIZE)
					.addGap(0, 16, GroupLayout.PREFERRED_SIZE)
					.addComponent(listOfBooksRequestedFromCentralLibraryMarkAsReceivedButton, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
					.addContainerGap(18, 18));
			}
			//KeeperGUI.this.setVisible(true);

		}
	}
	
	private class LendBookListener implements ActionListener{
		public void actionPerformed(ActionEvent e){
			KeeperGUI.this.centre.removeAll();
			String choiceList[]  = {"Search by ISBN", "Search by Title", "Search by Publisher","Search by Year",
					"Search By Author",	"Search by Book ID"};
			//start
			{
				lendBookPanel = new JPanel();
				GroupLayout lendBookPanelLayout = new GroupLayout((JComponent)lendBookPanel);
				lendBookPanel.setLayout(lendBookPanelLayout);
				KeeperGUI.this.centre.add(lendBookPanel);
				lendBookPanel.setPreferredSize(new java.awt.Dimension(466, 473));
				{
					tabbedPaneForTheSearch = new JTabbedPane();
					{
						searchForBookPanelInsideJPane = new JPanel();
						GroupLayout searchForBookPanelInsideJPaneLayout = new GroupLayout((JComponent)searchForBookPanelInsideJPane);
						searchForBookPanelInsideJPane.setLayout(searchForBookPanelInsideJPaneLayout);
						tabbedPaneForTheSearch.addTab("search for book", null, searchForBookPanelInsideJPane, null);
						{
							ComboBoxModel bookCriteriaModel = 
								new DefaultComboBoxModel(choiceList);
							bookCriteria = new JComboBox();
							bookCriteria.setModel(bookCriteriaModel);
							bookCriteria.setSelectedIndex(0);
						}
						{
							searchBoxForBook = new JTextField();
						}
						{
							bookResultScrollPane = new JScrollPane();
						}
						{
							jButton1 = new JButton();
							jButton1.setText("Search");
						}
						searchForBookPanelInsideJPaneLayout.setHorizontalGroup(searchForBookPanelInsideJPaneLayout.createSequentialGroup()
							.addContainerGap()
							.addGroup(searchForBookPanelInsideJPaneLayout.createParallelGroup()
							    .addGroup(GroupLayout.Alignment.LEADING, searchForBookPanelInsideJPaneLayout.createSequentialGroup()
							        .addComponent(bookCriteria, GroupLayout.PREFERRED_SIZE, 162, GroupLayout.PREFERRED_SIZE)
							        .addGap(29)
							        .addGroup(searchForBookPanelInsideJPaneLayout.createParallelGroup()
							            .addGroup(searchForBookPanelInsideJPaneLayout.createSequentialGroup()
							                .addComponent(searchBoxForBook, GroupLayout.PREFERRED_SIZE, 167, GroupLayout.PREFERRED_SIZE)
							                .addGap(0, 0, Short.MAX_VALUE))
							            .addGroup(GroupLayout.Alignment.LEADING, searchForBookPanelInsideJPaneLayout.createSequentialGroup()
							                .addGap(28)
							                .addComponent(jButton1, GroupLayout.PREFERRED_SIZE, 110, GroupLayout.PREFERRED_SIZE)
							                .addGap(0, 29, Short.MAX_VALUE))))
							    .addComponent(bookResultScrollPane, GroupLayout.Alignment.LEADING, 0, 358, Short.MAX_VALUE))
							.addContainerGap(24, 24));
						searchForBookPanelInsideJPaneLayout.setVerticalGroup(searchForBookPanelInsideJPaneLayout.createSequentialGroup()
							.addContainerGap(20, 20)
							.addGroup(searchForBookPanelInsideJPaneLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
							    .addComponent(bookCriteria, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
							    .addComponent(searchBoxForBook, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE))
							.addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
							.addComponent(jButton1, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
							.addGap(21)
							.addComponent(bookResultScrollPane, GroupLayout.PREFERRED_SIZE, 244, GroupLayout.PREFERRED_SIZE)
							.addContainerGap(25, Short.MAX_VALUE));
					}
					{
						searchForUserPanelInsideJPane = new JPanel();
						tabbedPaneForTheSearch.addTab("search for user", null, searchForUserPanelInsideJPane, null);
						{
							jPanel1 = new JPanel();
							searchForUserPanelInsideJPane.add(jPanel1);
							GroupLayout jPanel1Layout = new GroupLayout((JComponent)jPanel1);
							jPanel1.setLayout(jPanel1Layout);
							{
								ComboBoxModel jComboBox1Model = 
									new DefaultComboBoxModel(
											new String[] { "Search by User ID", "Search by Name" });
								jComboBox1 = new JComboBox();
								jComboBox1.setModel(jComboBox1Model);
							}
							{
								jTextField1 = new JTextField();
							}
							{
								jScrollPane1 = new JScrollPane();
							}
							{
								startSearchbutton = new JButton();
								startSearchbutton.setText("Search");
							}
								jPanel1Layout.setHorizontalGroup(jPanel1Layout.createSequentialGroup()
								.addContainerGap()
								.addGroup(jPanel1Layout.createParallelGroup()
								    .addGroup(GroupLayout.Alignment.LEADING, jPanel1Layout.createSequentialGroup()
								        .addComponent(jComboBox1, GroupLayout.PREFERRED_SIZE, 162, GroupLayout.PREFERRED_SIZE)
								        .addGap(29)
								        .addGroup(jPanel1Layout.createParallelGroup()
								            .addGroup(jPanel1Layout.createSequentialGroup()
								                .addComponent(jTextField1, GroupLayout.PREFERRED_SIZE, 167, GroupLayout.PREFERRED_SIZE)
								                .addGap(0, 0, Short.MAX_VALUE))
								            .addGroup(GroupLayout.Alignment.LEADING, jPanel1Layout.createSequentialGroup()
								                .addGap(37)
								                .addComponent(startSearchbutton, GroupLayout.PREFERRED_SIZE, 110, GroupLayout.PREFERRED_SIZE)
								                .addGap(0, 20, Short.MAX_VALUE))))
								    .addComponent(jScrollPane1, GroupLayout.Alignment.LEADING, 0, 358, Short.MAX_VALUE))
								.addContainerGap(24, 24));
								jPanel1Layout.setVerticalGroup(jPanel1Layout.createSequentialGroup()
								.addContainerGap(20, 20)
								.addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
								    .addComponent(jComboBox1, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
								    .addComponent(jTextField1, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE))
								.addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
								.addComponent(startSearchbutton, GroupLayout.PREFERRED_SIZE, 22, GroupLayout.PREFERRED_SIZE)
								.addGap(19)
								.addComponent(jScrollPane1, GroupLayout.PREFERRED_SIZE, 244, GroupLayout.PREFERRED_SIZE)
								.addContainerGap(25, Short.MAX_VALUE));
						}
					}
				}
				{
					approveLoanButtonInsideLendBookSubPanelofCentrePanel = new JButton();
					approveLoanButtonInsideLendBookSubPanelofCentrePanel.setText("Approve Loan");
				}
					lendBookPanelLayout.setHorizontalGroup(lendBookPanelLayout.createSequentialGroup()
					.addContainerGap(31, 31)
					.addGroup(lendBookPanelLayout.createParallelGroup()
					    .addGroup(lendBookPanelLayout.createSequentialGroup()
					        .addComponent(tabbedPaneForTheSearch, GroupLayout.PREFERRED_SIZE, 399, GroupLayout.PREFERRED_SIZE)
					        .addGap(0, 0, Short.MAX_VALUE))
					    .addGroup(GroupLayout.Alignment.LEADING, lendBookPanelLayout.createSequentialGroup()
					        .addGap(110)
					        .addComponent(approveLoanButtonInsideLendBookSubPanelofCentrePanel, GroupLayout.PREFERRED_SIZE, 167, GroupLayout.PREFERRED_SIZE)
					        .addGap(0, 122, Short.MAX_VALUE)))
					.addContainerGap(36, 36));
					lendBookPanelLayout.setVerticalGroup(lendBookPanelLayout.createSequentialGroup()
					.addContainerGap(26, 26)
					.addComponent(tabbedPaneForTheSearch, GroupLayout.PREFERRED_SIZE, 394, GroupLayout.PREFERRED_SIZE)
					.addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
					.addComponent(approveLoanButtonInsideLendBookSubPanelofCentrePanel, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
					.addContainerGap(19, Short.MAX_VALUE));
			}
			
		}
	}
	
	private class UserSearchListener implements ActionListener{
		public void actionPerformed(ActionEvent e){
			KeeperGUI.this.centre.removeAll();
			//start
			{
				searchForUSerPanel = new JPanel();
				GroupLayout searchForUSerPanelLayout = new GroupLayout((JComponent)searchForUSerPanel);
				searchForUSerPanel.setLayout(searchForUSerPanelLayout);
				KeeperGUI.this.centre.add(searchForUSerPanel);
				searchForUSerPanel.setPreferredSize(new java.awt.Dimension(479, 463));
				{
					searchInitiatorButton = new JButton();
					searchInitiatorButton.setText("Search");
				}
				{
					whateverYourCriteriaIsFiel = new JTextField();
				}
				{
					ComboBoxModel userSearchCriteriaChoiceListModel = 
						new DefaultComboBoxModel(
								new String[] { "Item One", "Item Two" });
					userSearchCriteriaChoiceList = new JComboBox();
					userSearchCriteriaChoiceList.setModel(userSearchCriteriaChoiceListModel);
				}
				{
					userSearchResultScrollPane = new JScrollPane();
				}
				//TODO add and remove keeper went here
				{
					requestReturnOfABookInTheList = new JButton();
					requestReturnOfABookInTheList.setText("Request return");
					requestReturnOfABookInTheList.setToolTipText("Request that the book selected in the list is returned");
				}
				searchForUSerPanelLayout.setHorizontalGroup(searchForUSerPanelLayout.createSequentialGroup()
					.addContainerGap(32, 32)
					.addGroup(searchForUSerPanelLayout.createParallelGroup()
					    .addGroup(GroupLayout.Alignment.LEADING, searchForUSerPanelLayout.createSequentialGroup()
					        .addComponent(userSearchCriteriaChoiceList, GroupLayout.PREFERRED_SIZE, 166, GroupLayout.PREFERRED_SIZE)
					        .addGap(40)
					        .addComponent(whateverYourCriteriaIsFiel, GroupLayout.PREFERRED_SIZE, 219, GroupLayout.PREFERRED_SIZE)
					        .addGap(0, 0, Short.MAX_VALUE))
					    .addComponent(userSearchResultScrollPane, GroupLayout.Alignment.LEADING, 0, 425, Short.MAX_VALUE)
					    .addGroup(GroupLayout.Alignment.LEADING, searchForUSerPanelLayout.createSequentialGroup()
					        .addComponent(addKeeperButton, GroupLayout.PREFERRED_SIZE, 122, GroupLayout.PREFERRED_SIZE)
					        .addGap(0, 19, Short.MAX_VALUE)
					        .addComponent(removeKeeperButton, GroupLayout.PREFERRED_SIZE, 120, GroupLayout.PREFERRED_SIZE)
					        .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
					        .addGroup(searchForUSerPanelLayout.createParallelGroup()
					            .addComponent(requestReturnOfABookInTheList, GroupLayout.Alignment.LEADING, GroupLayout.PREFERRED_SIZE, 142, GroupLayout.PREFERRED_SIZE)
					            .addGroup(GroupLayout.Alignment.LEADING, searchForUSerPanelLayout.createSequentialGroup()
					                .addComponent(searchInitiatorButton, GroupLayout.PREFERRED_SIZE, 130, GroupLayout.PREFERRED_SIZE)
					                .addGap(0, 12, GroupLayout.PREFERRED_SIZE)))
					        .addGap(11)))
					.addContainerGap(22, 22));
				searchForUSerPanelLayout.setVerticalGroup(searchForUSerPanelLayout.createSequentialGroup()
					.addContainerGap()
					.addGroup(searchForUSerPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
					    .addComponent(whateverYourCriteriaIsFiel, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
					    .addComponent(userSearchCriteriaChoiceList, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE))
					.addGap(31)
					.addComponent(searchInitiatorButton, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
					.addGap(19)
					.addComponent(userSearchResultScrollPane, GroupLayout.PREFERRED_SIZE, 310, GroupLayout.PREFERRED_SIZE)
					.addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
					.addGroup(searchForUSerPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
					    .addComponent(requestReturnOfABookInTheList, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
					    .addComponent(addKeeperButton, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE)
					    .addComponent(removeKeeperButton, GroupLayout.Alignment.BASELINE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE, GroupLayout.PREFERRED_SIZE))
					.addContainerGap());
			}
			//end
		}
	}
}
