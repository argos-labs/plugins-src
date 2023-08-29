namespace windnd
{
    partial class PWForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(PWForm));
            this.lbTitle = new System.Windows.Forms.Label();
            this.tbPasswd = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // lbTitle
            // 
            this.lbTitle.Dock = System.Windows.Forms.DockStyle.Top;
            this.lbTitle.Font = new System.Drawing.Font("Segoe UI", 10.125F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbTitle.Location = new System.Drawing.Point(0, 0);
            this.lbTitle.Name = "lbTitle";
            this.lbTitle.Size = new System.Drawing.Size(674, 95);
            this.lbTitle.TabIndex = 1;
            this.lbTitle.Text = "Enter password for the user \"{user}\" to allow drag and drop from other user appli" +
    "cation.  ";
            this.lbTitle.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            // 
            // tbPasswd
            // 
            this.tbPasswd.Location = new System.Drawing.Point(111, 128);
            this.tbPasswd.Name = "tbPasswd";
            this.tbPasswd.PasswordChar = '*';
            this.tbPasswd.Size = new System.Drawing.Size(464, 43);
            this.tbPasswd.TabIndex = 2;
            this.tbPasswd.KeyDown += new System.Windows.Forms.KeyEventHandler(this.tbPasswd_KeyDown);
            // 
            // PWForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(15F, 37F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(674, 229);
            this.Controls.Add(this.tbPasswd);
            this.Controls.Add(this.lbTitle);
            this.Font = new System.Drawing.Font("Segoe UI", 10.125F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(3, 5, 3, 5);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "PWForm";
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.Text = "Enter Password";
            this.Load += new System.EventHandler(this.PWForm_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lbTitle;
        private System.Windows.Forms.TextBox tbPasswd;
    }
}