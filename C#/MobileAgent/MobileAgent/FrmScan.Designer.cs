namespace MobileAgent
{
    partial class FrmScan
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.MainMenu mainMenu1;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.mainMenu1 = new System.Windows.Forms.MainMenu();
            this.txtBoard = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // txtBoard
            // 
            this.txtBoard.Font = new System.Drawing.Font("Tahoma", 8F, System.Drawing.FontStyle.Regular);
            this.txtBoard.Location = new System.Drawing.Point(17, 3);
            this.txtBoard.Multiline = true;
            this.txtBoard.Name = "txtBoard";
            this.txtBoard.ReadOnly = true;
            this.txtBoard.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.txtBoard.Size = new System.Drawing.Size(201, 236);
            this.txtBoard.TabIndex = 0;
            this.txtBoard.WordWrap = false;
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(84, 245);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(72, 20);
            this.button1.TabIndex = 1;
            this.button1.Text = "Scan";
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // FrmScan
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(96F, 96F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Dpi;
            this.AutoScroll = true;
            this.ClientSize = new System.Drawing.Size(240, 268);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.txtBoard);
            this.Menu = this.mainMenu1;
            this.Name = "FrmScan";
            this.Text = "Mobile Agent";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TextBox txtBoard;
        private System.Windows.Forms.Button button1;
    }
}

