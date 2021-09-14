
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import javax.swing.*;
import javax.swing.JFrame;

/*
 * This is a Base class that can be used for your Final Exam.
 */
/**
 *
 * @author smv159
 */
public class FinalBase extends JFrame {

    public JButton submit_btn;
    public JLabel name_label;
    public JTextField name_txt;
    public JComboBox combo_1;
    public JComboBox combo_2;
    public JComboBox combo_3;
    public JTextField combo1_txt;
    public JTextField combo2_txt;
    public JTextField combo3_txt;

    JPanel name_pane;
    JPanel combo_pane;

    public String[] combo_select = {"Select one from following", "Outfits", "Attributes", "Weapons"};

    public FinalBase() {
        initComponents();
    }

    public void initComponents() {
        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("Final Exam Base");
        setPreferredSize(new Dimension(460, 400));
        setLayout(new FlowLayout());

        name_pane = new JPanel(new FlowLayout());

        name_label = new JLabel("Inut the name of your character: ");
        name_txt = new JTextField(10);
        name_txt.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
            }
        });

        name_pane.add(name_label);
        name_pane.add(name_txt);

        combo_1 = new JComboBox(combo_select);
        combo_1.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {

            }
        });
        combo1_txt = new JTextField(20);

        combo_2 = new JComboBox(combo_select);
        combo_2.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {

            }
        });
        combo2_txt = new JTextField(20);

        combo_3 = new JComboBox(combo_select);
        combo_3.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {

            }
        });
        combo3_txt = new JTextField(20);

        submit_btn = new JButton();
        submit_btn.setText("Submit");
        submit_btn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.out.println("Submit Button was pressed.");

                //System.out.println(getWidth()+" "+getHeight());
                if (combo_1.getSelectedIndex() != 0 && combo_2.getSelectedIndex() != 0 && combo_3.getSelectedIndex() != 0 && (combo_1.getSelectedIndex() + combo_2.getSelectedIndex() + combo_3.getSelectedIndex()) != 3 * combo_1.getSelectedIndex()) {
                    String t1 = combo_1.getSelectedItem().toString().toLowerCase();
                    String v1 = combo1_txt.getText();
                    String t2 = combo_2.getSelectedItem().toString().toLowerCase();
                    String v2 = combo2_txt.getText();
                    String t3 = combo_3.getSelectedItem().toString().toLowerCase();
                    String v3 = combo3_txt.getText();

                    System.out.println("The name of character is: " + name_txt.getText()
                            + ", the " + t1 + " is: " + v1
                            + ", the " + t2 + " is: " + v2
                            + ", and the " + t3 + " is: " + v3 + ".");
                    sql_inter sql = new sql_inter();
                        String query = "insert into " + t1 + " (description) values ('"
                                + v1 + "')";
                        sql.insert(query);
                        query = "insert into " + t2 + " (description) values ('"
                                + v2 + "')";
                        sql.insert(query);
                        query = "insert into " + t3 + " (description) values ('"
                                + v3 + "')";
                        sql.insert(query);
                    
                    query = "insert into characters (name) values ('"
                            + name_txt.getText()+"')";
                    sql.insert(query);
                    
                    
                    sql.close();

                } else {
                    JOptionPane.showMessageDialog(null, "You have to select all three\n And one thing can only be selected one time", "Warning", JOptionPane.WARNING_MESSAGE);
                }

                name_txt.setText("");
                combo_1.setSelectedIndex(0);
                combo_2.setSelectedIndex(0);
                combo_3.setSelectedIndex(0);
                combo1_txt.setText("");
                combo2_txt.setText("");
                combo3_txt.setText("");
                
            }
        });

        getContentPane().add(name_pane);

        getContentPane().add(combo_1);
        getContentPane().add(combo1_txt);
        getContentPane().add(combo_2);
        getContentPane().add(combo2_txt);
        getContentPane().add(combo_3);
        getContentPane().add(combo3_txt);
        getContentPane().add(submit_btn);

        pack();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        // Create and display the form
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new FinalBase().setVisible(true);
            }
        });
    }
}
