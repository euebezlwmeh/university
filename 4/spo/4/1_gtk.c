#include <gtk/gtk.h>
#include <sqlite3.h>

static sqlite3 *db;
static GtkWidget *entry_id, *entry_name, *entry_dob, *entry_gender;

void on_add_button_clicked(GtkWidget *widget, gpointer data) {
    const char *sql = "INSERT INTO Employee (id, name, dob, gender) VALUES (?, ?, ?, ?)";
    sqlite3_stmt *stmt;
    
    sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    sqlite3_bind_int(stmt, 1, atoi(gtk_entry_get_text(GTK_ENTRY(entry_id))));
    sqlite3_bind_text(stmt, 2, gtk_entry_get_text(GTK_ENTRY(entry_name)), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, gtk_entry_get_text(GTK_ENTRY(entry_dob)), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 4, gtk_entry_get_text(GTK_ENTRY(entry_gender)), -1, SQLITE_STATIC);
    
    sqlite3_step(stmt);
    sqlite3_finalize(stmt);
}

void on_view_button_clicked(GtkWidget *widget, gpointer data) {
    // Реализация отображения данных из таблицы
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);
    
    // Открытие базы данных
    sqlite3_open("company.db", &db);
    
    // Создание GUI
    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Database Wrapper");
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    
    // Создание элементов интерфейса
    entry_id = gtk_entry_new();
    entry_name = gtk_entry_new();
    entry_dob = gtk_entry_new();
    entry_gender = gtk_entry_new();
    
    GtkWidget *add_button = gtk_button_new_with_label("Добавить");
    g_signal_connect(add_button, "clicked", G_CALLBACK(on_add_button_clicked), NULL);
    
    GtkWidget *view_button = gtk_button_new_with_label("Посмотреть");
    g_signal_connect(view_button, "clicked", G_CALLBACK(on_view_button_clicked), NULL);
    
    // Упаковка элементов в контейнер
    GtkWidget *vbox = gtk_vbox_new(FALSE, 5);
    gtk_box_pack_start(GTK_BOX(vbox), entry_id, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), entry_name, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), entry_dob, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), entry_gender, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), add_button, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(vbox), view_button, FALSE, FALSE, 0);
    
    gtk_container_add(GTK_CONTAINER(window), vbox);
    gtk_widget_show_all(window);
    
    gtk_main();
    
    // Закрытие базы данных
    sqlite3_close(db);
    
    return 0;
}
