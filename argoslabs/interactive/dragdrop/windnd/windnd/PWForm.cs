using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace windnd
{
    public partial class PWForm : Form
    {
        private string username;
        public string passwd { get; set; }

        public PWForm(string userName)
        {
            InitializeComponent();
            this.username = userName;
        }

        private void tbPasswd_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                this.passwd = tbPasswd.Text;
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
        }

        private void PWForm_Load(object sender, EventArgs e)
        {
            this.lbTitle.Text = this.lbTitle.Text.Replace("{user}", username);
            this.Width = 700;
            this.Height = 300;
        }
    }
}
