namespace windnd
{
    partial class Form1
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.panel2 = new System.Windows.Forms.Panel();
            this.lb = new System.Windows.Forms.Label();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.panel2.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.SuspendLayout();
            // 
            // panel2
            // 
            this.panel2.AllowDrop = true;
            this.panel2.Controls.Add(this.groupBox1);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel2.Location = new System.Drawing.Point(0, 0);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(874, 429);
            this.panel2.TabIndex = 2;
            // 
            // lb
            // 
            this.lb.AllowDrop = true;
            this.lb.BackColor = System.Drawing.SystemColors.Control;
            this.lb.Font = new System.Drawing.Font("Segoe UI", 10.125F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lb.Location = new System.Drawing.Point(6, 17);
            this.lb.Name = "lb";
            this.lb.Size = new System.Drawing.Size(812, 379);
            this.lb.TabIndex = 0;
            this.lb.Text = "Drop your file here!";
            this.lb.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.lb.UseMnemonic = false;
            this.lb.DragDrop += new System.Windows.Forms.DragEventHandler(this.lb_DragDrop);
            this.lb.DragEnter += new System.Windows.Forms.DragEventHandler(this.lb_DragEnter);
            this.lb.DragOver += new System.Windows.Forms.DragEventHandler(this.lb_DragOver);
            this.lb.DragLeave += new System.EventHandler(this.lb_DragLeave);
            this.lb.GiveFeedback += new System.Windows.Forms.GiveFeedbackEventHandler(this.lb_GiveFeedback);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.lb);
            this.groupBox1.Location = new System.Drawing.Point(20, 18);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(850, 408);
            this.groupBox1.TabIndex = 1;
            this.groupBox1.TabStop = false;
            // 
            // Form1
            // 
            this.AllowDrop = true;
            this.AutoScaleDimensions = new System.Drawing.SizeF(13F, 24F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(874, 429);
            this.Controls.Add(this.panel2);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MaximumSize = new System.Drawing.Size(900, 500);
            this.MinimizeBox = false;
            this.MinimumSize = new System.Drawing.Size(900, 500);
            this.Name = "Form1";
            this.Text = "ARGOS Assist-o-mation";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.panel2.ResumeLayout(false);
            this.groupBox1.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Label lb;
        private System.Windows.Forms.GroupBox groupBox1;
    }
}

